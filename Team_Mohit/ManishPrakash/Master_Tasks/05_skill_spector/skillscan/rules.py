"""Detection rules for agent skill auditing.

Each rule is a regex plus the reasoning for why the pattern matters in the
specific context of an agent skill. The rationale is part of the rule, not
documentation about it: a finding a reviewer cannot act on is noise, and
"matched pattern 14" is not actionable.

Rules are grouped into families:

    EXECUTION      running code fetched or constructed at runtime
    CREDENTIALS    reading secrets the skill has no reason to touch
    EXFILTRATION   sending local data to a remote host
    DESTRUCTIVE    irreversible changes to the host
    PERSISTENCE    surviving beyond the current invocation
    OBFUSCATION    hiding what the code does
    INJECTION      prompt-injection directed at the reading model
    SUPPLY_CHAIN   unpinned or unverified third-party code

A rule matching does not mean a skill is malicious. It means a human should
look at that line. The tool ranks and explains; it does not adjudicate.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from enum import Enum


class Severity(str, Enum):
    """How urgently a human should look at a finding."""

    CRITICAL = "critical"  # arbitrary code execution or credential theft
    HIGH = "high"          # plausible path to either
    MEDIUM = "medium"      # risky but has legitimate uses
    LOW = "low"            # worth noting in review
    INFO = "info"          # context, not a concern

    @property
    def rank(self) -> int:
        return {
            Severity.CRITICAL: 4,
            Severity.HIGH: 3,
            Severity.MEDIUM: 2,
            Severity.LOW: 1,
            Severity.INFO: 0,
        }[self]


class Family(str, Enum):
    EXECUTION = "execution"
    CREDENTIALS = "credentials"
    EXFILTRATION = "exfiltration"
    DESTRUCTIVE = "destructive"
    PERSISTENCE = "persistence"
    OBFUSCATION = "obfuscation"
    INJECTION = "prompt-injection"
    SUPPLY_CHAIN = "supply-chain"
    NETWORK = "network"


@dataclass(frozen=True)
class Rule:
    """One detection pattern."""

    id: str
    name: str
    family: Family
    severity: Severity
    pattern: re.Pattern[str]
    rationale: str
    # Rules that only make sense in prose (SKILL.md) rather than code.
    prose_only: bool = False

    def search(self, line: str) -> re.Match[str] | None:
        return self.pattern.search(line)


def _c(pattern: str) -> re.Pattern[str]:
    return re.compile(pattern, re.IGNORECASE)


RULES: tuple[Rule, ...] = (
    # -- EXECUTION ---------------------------------------------------------
    Rule(
        "EXEC001",
        "Pipe from network directly to a shell",
        Family.EXECUTION,
        Severity.CRITICAL,
        _c(r"(curl|wget)\b[^\n|]*\|\s*(sudo\s+)?(ba|z|k|d)?sh\b"),
        "Downloads and executes remote code in one step, with no opportunity to "
        "inspect it. Whatever is on that URL today may not be what is there "
        "tomorrow, and the skill has granted it your user's privileges.",
    ),
    Rule(
        "EXEC002",
        "Dynamic evaluation of a string",
        Family.EXECUTION,
        Severity.HIGH,
        _c(r"\b(eval|exec)\s*\("),
        "Executes code assembled at runtime. If any part of that string comes "
        "from a file, an argument, or model output, this is arbitrary code "
        "execution.",
    ),
    Rule(
        "EXEC003",
        "Shell invocation from code",
        Family.EXECUTION,
        Severity.MEDIUM,
        _c(r"\b(os\.system|subprocess\.(call|run|Popen|check_output)|child_process)\b"),
        "Spawns a shell. Legitimate in most skills, but every call site needs "
        "checking for unescaped interpolation of untrusted input.",
    ),
    Rule(
        "EXEC004",
        "Shell command built by string interpolation",
        Family.EXECUTION,
        Severity.HIGH,
        _c(r"(os\.system|subprocess\.\w+|exec\w*)\s*\(\s*f?[\"'][^\"']*\{|\$\{[^}]+\}[^\n]*\|\s*sh"),
        "A command constructed from a variable is a command injection unless "
        "every input is validated. Prefer an argument list over a shell string.",
    ),

    # -- CREDENTIALS -------------------------------------------------------
    Rule(
        "CRED001",
        "Access to SSH private keys",
        Family.CREDENTIALS,
        Severity.CRITICAL,
        _c(r"[~/\\.\w]*\.ssh/(id_\w+|identity)\b|\.ssh/id_rsa"),
        "Reads SSH private keys. Essentially no legitimate skill needs these, "
        "and possession of one is durable access to every host that trusts it.",
    ),
    Rule(
        "CRED002",
        "Access to cloud provider credentials",
        Family.CREDENTIALS,
        Severity.CRITICAL,
        _c(r"\.aws/credentials|\.config/gcloud|\.kube/config|\.docker/config\.json"),
        "Reads long-lived cloud or cluster credentials. Compromise here extends "
        "well beyond the machine the skill runs on.",
    ),
    Rule(
        "CRED003",
        "Reading environment or secret files",
        Family.CREDENTIALS,
        Severity.HIGH,
        _c(r"(open|read|cat|Path)\s*\(?\s*[\"'][^\"']*\.env\b|/\.env\b|\bdotenv_values\b"),
        "Reads a .env file, which by convention holds API keys. Check whether "
        "the skill needs the whole file or one named variable.",
    ),
    Rule(
        "CRED004",
        "Broad sweep of environment variables",
        Family.CREDENTIALS,
        Severity.MEDIUM,
        _c(r"(os\.environ(?!\s*(\.get)?\s*\[?\s*[\"']\w)|process\.env\s*[,)\]}]|dict\(os\.environ\))"),
        "Reading the whole environment rather than a named variable. Combined "
        "with any network call, this is credential exfiltration.",
    ),
    Rule(
        "CRED005",
        "Hard-coded secret",
        Family.CREDENTIALS,
        Severity.HIGH,
        _c(r"\b(api[_-]?key|secret|token|passwd|password)\s*[:=]\s*[\"'][A-Za-z0-9_\-]{16,}[\"']"),
        "A credential committed into the skill. It is exposed to everyone who "
        "installs it and cannot be rotated by them.",
    ),

    # -- EXFILTRATION ------------------------------------------------------
    Rule(
        "EXFIL001",
        "Outbound POST carrying a payload",
        Family.EXFILTRATION,
        Severity.HIGH,
        _c(
            r"\b(requests\.post|axios\.post|http\.post|session\.post)\s*\("
            r"|fetch\s*\([^)]*method\s*:\s*[\"']POST"
            r"|curl\b[^\n]*(-X\s*POST|\s-d\s|--data\b|-F\s)"
        ),
        "Sends a request body outward. Confirm what is in that body and that "
        "the destination is a host the skill legitimately belongs to.",
    ),
    Rule(
        "EXFIL002",
        "Raw IP address as a destination",
        Family.EXFILTRATION,
        Severity.HIGH,
        _c(r"https?://(\d{1,3}\.){3}\d{1,3}(:\d+)?"),
        "A bare IP address avoids DNS logging and domain reputation. Legitimate "
        "services almost always use a hostname.",
    ),
    Rule(
        "EXFIL003",
        "Data sent to a webhook or paste service",
        Family.EXFILTRATION,
        Severity.HIGH,
        _c(r"(webhook\.site|pastebin\.com|requestbin|ngrok\.io|transfer\.sh|0x0\.st|termbin)"),
        "These hosts exist to receive arbitrary data from anywhere. Their "
        "presence in a skill is difficult to explain innocently.",
    ),
    Rule(
        "EXFIL004",
        "Reverse shell pattern",
        Family.EXFILTRATION,
        Severity.CRITICAL,
        _c(r"(nc|ncat|netcat)\s+(-\w+\s+)*-\w*e|bash\s+-i\s*>&\s*/dev/tcp|socket\.socket\([^)]*\)[^\n]*connect"),
        "Opens an interactive channel back to a remote host. This is a backdoor; "
        "there is no benign reading of it in an agent skill.",
    ),

    # -- DESTRUCTIVE -------------------------------------------------------
    Rule(
        "DEST001",
        "Recursive force delete",
        Family.DESTRUCTIVE,
        Severity.CRITICAL,
        _c(r"rm\s+(-[a-z]*r[a-z]*f|-[a-z]*f[a-z]*r)\s+[\"']?(/|~|\$HOME|\*)"),
        "Recursive deletion rooted at the filesystem root or home directory. "
        "Irreversible, and a single wrong variable makes it catastrophic.",
    ),
    Rule(
        "DEST002",
        "Recursive tree removal from code",
        Family.DESTRUCTIVE,
        Severity.HIGH,
        _c(r"shutil\.rmtree|fs\.rm\w*\([^)]*recursive|os\.removedirs"),
        "Deletes a directory tree. Verify the target is inside the skill's own "
        "workspace and cannot be redirected by an argument.",
    ),
    Rule(
        "DEST003",
        "Overly permissive file mode",
        Family.DESTRUCTIVE,
        Severity.MEDIUM,
        _c(r"chmod\s+(-R\s+)?0?777|os\.chmod\([^)]*0o?777"),
        "World-writable permissions let any local process modify the file, "
        "including replacing a script this skill later executes.",
    ),
    Rule(
        "DEST004",
        "Disk or device write",
        Family.DESTRUCTIVE,
        Severity.CRITICAL,
        _c(r"\bdd\s+[^\n]*of=\s*/dev/|mkfs\.|>\s*/dev/[sh]d[a-z]"),
        "Writes directly to a block device. Destroys data below the filesystem "
        "level, where no backup of the running system will help.",
    ),

    # -- PERSISTENCE -------------------------------------------------------
    Rule(
        "PERS001",
        "Scheduled task installation",
        Family.PERSISTENCE,
        Severity.HIGH,
        _c(r"crontab\s+-|/etc/cron|systemctl\s+(enable|--user\s+enable)|launchctl\s+load"),
        "Arranges to run again after the skill finishes. Persistence is the "
        "difference between a one-time action and an ongoing presence.",
    ),
    Rule(
        "PERS002",
        "Shell profile modification",
        Family.PERSISTENCE,
        Severity.HIGH,
        _c(r">>\s*[~\w/\\.]*(\.bashrc|\.zshrc|\.profile|\.bash_profile|config\.fish)"),
        "Appends to a shell startup file, so the added code runs in every future "
        "shell the user opens.",
    ),
    Rule(
        "PERS003",
        "SSH authorized_keys modification",
        Family.PERSISTENCE,
        Severity.CRITICAL,
        _c(r"authorized_keys"),
        "Writing here grants durable remote login to whoever holds the matching "
        "private key.",
    ),

    # -- OBFUSCATION -------------------------------------------------------
    Rule(
        "OBF001",
        "Base64 decode feeding execution",
        Family.OBFUSCATION,
        Severity.CRITICAL,
        _c(r"(base64\s+(-d|--decode)|b64decode|atob|Buffer\.from\([^)]*base64)"),
        "Encoded payloads exist to defeat review. Combined with any execution "
        "primitive this is a deliberate attempt to hide behaviour.",
    ),
    Rule(
        "OBF002",
        "Hex or escape-encoded string blob",
        Family.OBFUSCATION,
        Severity.MEDIUM,
        _c(r"(\\x[0-9a-f]{2}){8,}"),
        "A long escape-encoded literal is unreadable to a reviewer, which is "
        "usually the point.",
    ),
    Rule(
        "OBF003",
        "Character-code string reconstruction",
        Family.OBFUSCATION,
        Severity.MEDIUM,
        _c(r"(chr\(\d+\)\s*\+\s*){3,}|String\.fromCharCode"),
        "Rebuilding a string from character codes hides it from both a reader "
        "and a naive grep.",
    ),

    # -- INJECTION (SKILL.md prose) ---------------------------------------
    Rule(
        "INJ001",
        "Instruction to disregard prior guidance",
        Family.INJECTION,
        Severity.CRITICAL,
        _c(r"ignore\s+(all\s+)?(previous|prior|above|earlier)\s+(instructions?|prompts?|rules?)"),
        "A skill description is read by the model as instruction. Text telling it "
        "to discard its operating rules is a prompt-injection payload aimed at "
        "the agent, not documentation for a human.",
        prose_only=True,
    ),
    Rule(
        "INJ002",
        "Instruction to bypass confirmation or safety",
        Family.INJECTION,
        Severity.CRITICAL,
        _c(r"(without|skip|bypass|no need for|do not)\s+(asking|ask|prompting|confirm\w*|permission|approval)"),
        "Attempts to remove the human approval step that bounds what an agent "
        "can do irreversibly.",
        prose_only=True,
    ),
    Rule(
        "INJ003",
        "Instruction to conceal actions from the user",
        Family.INJECTION,
        Severity.CRITICAL,
        _c(r"(do\s*n[o']?t|never|avoid)\s+(tell|inform|mention|show|reveal|disclose|report)\w*\s+(to\s+)?the\s+(user|human|operator)"),
        "Directs the agent to hide what it is doing. Concealment has no "
        "legitimate purpose in a tool the user installed deliberately.",
        prose_only=True,
    ),
    Rule(
        "INJ004",
        "Hidden or invisible instruction text",
        Family.INJECTION,
        Severity.HIGH,
        _c(r"<!--[^>]*\b(ignore|instead|secret|do not tell|actually)\b|[​‌‍﻿]"),
        "Instructions in HTML comments or zero-width characters are invisible to "
        "a human reviewer but fully visible to the model reading the file.",
        prose_only=True,
    ),
    Rule(
        "INJ005",
        "Claimed elevated authority",
        Family.INJECTION,
        Severity.HIGH,
        _c(r"(you\s+are\s+now|from\s+now\s+on|new\s+(system\s+)?(instructions?|rules?)|override\s+\w*\s*instructions?|developer\s+mode)"),
        "Impersonates a higher-priority instruction source to displace the "
        "agent's real configuration.",
        prose_only=True,
    ),

    # -- SUPPLY CHAIN ------------------------------------------------------
    Rule(
        "SUP001",
        "Unpinned remote package execution",
        Family.SUPPLY_CHAIN,
        Severity.MEDIUM,
        _c(r"npx\s+(-y|--yes)|uvx\s+|pipx\s+run\s"),
        "Fetches and runs the latest published version on every launch. Today's "
        "review does not cover tomorrow's run.",
    ),
    Rule(
        "SUP002",
        "Install from a git URL or archive",
        Family.SUPPLY_CHAIN,
        Severity.MEDIUM,
        _c(r"pip\s+install\s+(git\+|https?://)|npm\s+i(nstall)?\s+(git\+|https?://)"),
        "Bypasses the package registry, so there is no published provenance and "
        "no version to audit.",
    ),
    Rule(
        "SUP003",
        "TLS verification disabled",
        Family.SUPPLY_CHAIN,
        Severity.HIGH,
        _c(r"verify\s*=\s*False|--no-check-certificate|curl\s+[^\n]*\s-k\b|rejectUnauthorized:\s*false|NODE_TLS_REJECT_UNAUTHORIZED"),
        "Turns off certificate checking, which is what makes an intercepted "
        "download indistinguishable from a genuine one.",
    ),

    # -- NETWORK -----------------------------------------------------------
    Rule(
        "NET001",
        "Outbound network call",
        Family.NETWORK,
        Severity.LOW,
        _c(r"\b(requests\.(get|put|patch|delete)|urlopen|urlretrieve|httpx\.\w+)\s*\("),
        "The skill talks to the network. Not a problem in itself; noted so the "
        "review covers what leaves the machine.",
    ),
)


RULES_BY_ID: dict[str, Rule] = {rule.id: rule for rule in RULES}


def rules_for(is_prose: bool) -> tuple[Rule, ...]:
    """Rules applicable to a file, split by whether it is prose or code.

    Prose-only rules would misfire constantly against source code, where
    phrases like "do not ask" appear in comments and string literals for
    entirely ordinary reasons.
    """
    if is_prose:
        return RULES
    return tuple(r for r in RULES if not r.prose_only)
