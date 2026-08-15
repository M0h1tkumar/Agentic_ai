# SkillSpector Security Report

**Skill:** unknown  
**Source:** `C:\TestSkills\agent-skills`  
**Scanned:** 2026-07-27 18:01:21 UTC  

## Risk Assessment

| Metric | Value |
|--------|-------|
| Score | 100/100 |
| Severity | CRITICAL |
| Recommendation | DO NOT INSTALL |

## Components (174)

| File | Type | Lines | Executable |
|------|------|-------|------------|
| `.agents/plugins/marketplace.json` | json | 21 | No |
| `.claude-plugin/marketplace.json` | json | 22 | No |
| `.claude-plugin/plugin.json` | json | 18 | No |
| `.claude/commands/build.md` | markdown | 44 | No |
| `.claude/commands/code-simplify.md` | markdown | 22 | No |
| `.claude/commands/plan.md` | markdown | 16 | No |
| `.claude/commands/review.md` | markdown | 16 | No |
| `.claude/commands/ship.md` | markdown | 72 | No |
| `.claude/commands/spec.md` | markdown | 15 | No |
| `.claude/commands/test.md` | markdown | 19 | No |
| `.claude/commands/webperf.md` | markdown | 32 | No |
| `.claude/rules/skills-contributing.md` | markdown | 15 | No |
| `.codex-plugin/plugin.json` | json | 21 | No |
| `.gemini/commands/build.toml` | toml | 43 | No |
| `.gemini/commands/code-simplify.toml` | toml | 22 | No |
| `.gemini/commands/planning.toml` | toml | 16 | No |
| `.gemini/commands/review.toml` | toml | 16 | No |
| `.gemini/commands/ship.toml` | toml | 72 | No |
| `.gemini/commands/spec.toml` | toml | 15 | No |
| `.gemini/commands/test.toml` | toml | 19 | No |
| `.gemini/commands/webperf.toml` | toml | 32 | No |
| `.github/ISSUE_TEMPLATE/skill-gap.yml` | yaml | 80 | No |
| `.github/workflows/test-plugin-install.yml` | yaml | 76 | No |
| `.opencode/skills` | other | 1 | No |
| `AGENTS.md` | markdown | 92 | No |
| `CLAUDE.md` | markdown | 60 | No |
| `CONTRIBUTING.md` | markdown | 123 | No |
| `LICENSE` | other | 21 | No |
| `README.md` | markdown | 402 | No |
| `agents/code-reviewer.md` | markdown | 97 | No |
| `agents/security-auditor.md` | markdown | 112 | No |
| `agents/test-engineer.md` | markdown | 95 | No |
| `agents/web-performance-auditor.md` | markdown | 184 | No |
| `commands/build.toml` | toml | 43 | No |
| `commands/code-simplify.toml` | toml | 22 | No |
| `commands/planning.toml` | toml | 16 | No |
| `commands/review.toml` | toml | 16 | No |
| `commands/ship.toml` | toml | 72 | No |
| `commands/spec.toml` | toml | 15 | No |
| `commands/test.toml` | toml | 19 | No |
| `commands/webperf.toml` | toml | 32 | No |
| `docs/adoption-guide.md` | markdown | 129 | No |
| `docs/agents.md` | markdown | 123 | No |
| `docs/antigravity-setup.md` | markdown | 123 | No |
| `docs/codex-setup.md` | markdown | 31 | No |
| `docs/comparison.md` | markdown | 129 | No |
| `docs/copilot-setup.md` | markdown | 87 | No |
| `docs/cursor-setup.md` | markdown | 225 | No |
| `docs/developer-onboarding.md` | markdown | 116 | No |
| `docs/gemini-cli-setup.md` | markdown | 132 | No |
| `docs/getting-started.md` | markdown | 157 | No |
| `docs/opencode-setup.md` | markdown | 178 | No |
| `docs/skill-anatomy.md` | markdown | 182 | No |
| `docs/windsurf-setup.md` | markdown | 48 | No |
| `evals/README.md` | markdown | 85 | No |
| `evals/cases/api-and-interface-design.json` | json | 45 | No |
| `evals/cases/browser-testing-with-devtools.json` | json | 44 | No |
| `evals/cases/ci-cd-and-automation.json` | json | 45 | No |
| `evals/cases/code-review-and-quality.json` | json | 45 | No |
| `evals/cases/code-simplification.json` | json | 44 | No |
| `evals/cases/context-engineering.json` | json | 44 | No |
| `evals/cases/debugging-and-error-recovery.json` | json | 58 | No |
| `evals/cases/deprecation-and-migration.json` | json | 43 | No |
| `evals/cases/documentation-and-adrs.json` | json | 44 | No |
| `evals/cases/doubt-driven-development.json` | json | 42 | No |
| `evals/cases/frontend-ui-engineering.json` | json | 51 | No |
| `evals/cases/git-workflow-and-versioning.json` | json | 43 | No |
| `evals/cases/idea-refine.json` | json | 43 | No |
| `evals/cases/incremental-implementation.json` | json | 57 | No |
| `evals/cases/interview-me.json` | json | 42 | No |
| `evals/cases/observability-and-instrumentation.json` | json | 44 | No |
| `evals/cases/performance-optimization.json` | json | 52 | No |
| `evals/cases/planning-and-task-breakdown.json` | json | 44 | No |
| `evals/cases/security-and-hardening.json` | json | 45 | No |
| `evals/cases/shipping-and-launch.json` | json | 56 | No |
| `evals/cases/source-driven-development.json` | json | 44 | No |
| `evals/cases/spec-driven-development.json` | json | 45 | No |
| `evals/cases/test-driven-development.json` | json | 72 | No |
| `evals/cases/using-agent-skills.json` | json | 43 | No |
| `evals/fixtures/api-and-interface-design/service-brief.md` | markdown | 19 | No |
| `evals/fixtures/browser-testing-with-devtools/README.md` | markdown | 5 | No |
| `evals/fixtures/browser-testing-with-devtools/index.html` | other | 24 | No |
| `evals/fixtures/browser-testing-with-devtools/server.js` | javascript | 15 | Yes |
| `evals/fixtures/ci-cd-and-automation/package.json` | json | 8 | No |
| `evals/fixtures/ci-cd-and-automation/src/slug.js` | javascript | 3 | Yes |
| `evals/fixtures/ci-cd-and-automation/test/slug.test.js` | javascript | 9 | Yes |
| `evals/fixtures/code-review-and-quality/user-search.diff` | other | 16 | No |
| `evals/fixtures/code-simplification/config-parser.js` | javascript | 46 | Yes |
| `evals/fixtures/code-simplification/config-parser.test.js` | javascript | 15 | Yes |
| `evals/fixtures/context-engineering/context-audit.md` | markdown | 15 | No |
| `evals/fixtures/debugging-and-error-recovery/pagination.js` | javascript | 8 | Yes |
| `evals/fixtures/debugging-and-error-recovery/pagination.test.js` | javascript | 9 | Yes |
| `evals/fixtures/debugging-and-error-recovery/time-pressure.md` | markdown | 6 | No |
| `evals/fixtures/deprecation-and-migration/api-inventory.md` | markdown | 9 | No |
| `evals/fixtures/documentation-and-adrs/decision-context.md` | markdown | 16 | No |
| `evals/fixtures/doubt-driven-development/migration-plan.md` | markdown | 19 | No |
| `evals/fixtures/frontend-ui-engineering/Button.tsx` | other | 7 | No |
| `evals/fixtures/frontend-ui-engineering/design-system.md` | markdown | 11 | No |
| `evals/fixtures/git-workflow-and-versioning/.eval/working-tree.patch` | other | 21 | No |
| `evals/fixtures/git-workflow-and-versioning/app.js` | javascript | 7 | Yes |
| `evals/fixtures/git-workflow-and-versioning/app.test.js` | javascript | 9 | Yes |
| `evals/fixtures/incremental-implementation-pressure/draft-export.js` | javascript | 17 | Yes |
| `evals/fixtures/incremental-implementation-pressure/scenario.md` | markdown | 9 | No |
| `evals/fixtures/incremental-implementation/reports.js` | javascript | 7 | Yes |
| `evals/fixtures/incremental-implementation/reports.test.js` | javascript | 12 | Yes |
| `evals/fixtures/incremental-implementation/tasks/plan.md` | markdown | 8 | No |
| `evals/fixtures/observability-and-instrumentation/operations.md` | markdown | 11 | No |
| `evals/fixtures/observability-and-instrumentation/payment-retry.js` | javascript | 14 | Yes |
| `evals/fixtures/performance-optimization/benchmark.js` | javascript | 15 | Yes |
| `evals/fixtures/performance-optimization/products.js` | javascript | 14 | Yes |
| `evals/fixtures/planning-and-task-breakdown/notifications-spec.md` | markdown | 18 | No |
| `evals/fixtures/security-and-hardening/webhook.js` | javascript | 11 | Yes |
| `evals/fixtures/security-and-hardening/webhook.test.js` | javascript | 13 | Yes |
| `evals/fixtures/shipping-and-launch/authority-pressure.md` | markdown | 6 | No |
| `evals/fixtures/shipping-and-launch/launch-status.md` | markdown | 11 | No |
| `evals/fixtures/source-driven-development/framework-task.md` | markdown | 10 | No |
| `evals/fixtures/spec-driven-development/billing-brief.md` | markdown | 16 | No |
| `evals/fixtures/test-driven-development-ecosystem/README.md` | markdown | 9 | No |
| `evals/fixtures/test-driven-development-ecosystem/ledger.py` | python | 15 | Yes |
| `evals/fixtures/test-driven-development-ecosystem/test_ledger.py` | python | 19 | Yes |
| `evals/fixtures/test-driven-development/authority-pressure.md` | markdown | 8 | No |
| `evals/fixtures/test-driven-development/invoice.js` | javascript | 7 | Yes |
| `evals/fixtures/test-driven-development/invoice.test.js` | javascript | 12 | Yes |
| `evals/fixtures/using-agent-skills/incident.md` | markdown | 6 | No |
| `hooks/SDD-CACHE.md` | markdown | 167 | No |
| `hooks/SIMPLIFY-IGNORE.md` | markdown | 90 | No |
| `hooks/hooks.json` | json | 14 | No |
| `hooks/sdd-cache-post.sh` | shell | 135 | Yes |
| `hooks/sdd-cache-pre.sh` | shell | 106 | Yes |
| `hooks/session-start-test.sh` | shell | 46 | Yes |
| `hooks/session-start.sh` | shell | 24 | Yes |
| `hooks/simplify-ignore-test.sh` | shell | 253 | Yes |
| `hooks/simplify-ignore.sh` | shell | 302 | Yes |
| `plugin.json` | json | 5 | No |
| `references/accessibility-checklist.md` | markdown | 160 | No |
| `references/definition-of-done.md` | markdown | 67 | No |
| `references/observability-checklist.md` | markdown | 91 | No |
| `references/orchestration-patterns.md` | markdown | 370 | No |
| `references/performance-checklist.md` | markdown | 153 | No |
| `references/security-checklist.md` | markdown | 205 | No |
| `references/testing-patterns.md` | markdown | 235 | No |
| `scripts/lib/skill-lint.js` | javascript | 250 | Yes |
| `scripts/run-evals-test.js` | javascript | 236 | Yes |
| `scripts/run-evals.js` | javascript | 561 | Yes |
| `scripts/validate-commands.js` | javascript | 187 | Yes |
| `scripts/validate-skills.js` | javascript | 69 | Yes |
| `skills/api-and-interface-design/SKILL.md` | markdown | 294 | No |
| `skills/browser-testing-with-devtools/SKILL.md` | markdown | 317 | No |
| `skills/ci-cd-and-automation/SKILL.md` | markdown | 390 | No |
| `skills/code-review-and-quality/SKILL.md` | markdown | 396 | No |
| `skills/code-simplification/SKILL.md` | markdown | 331 | No |
| `skills/context-engineering/SKILL.md` | markdown | 289 | No |
| `skills/debugging-and-error-recovery/SKILL.md` | markdown | 300 | No |
| `skills/deprecation-and-migration/SKILL.md` | markdown | 247 | No |
| `skills/documentation-and-adrs/SKILL.md` | markdown | 288 | No |
| `skills/doubt-driven-development/SKILL.md` | markdown | 243 | No |
| `skills/frontend-ui-engineering/SKILL.md` | markdown | 328 | No |
| `skills/git-workflow-and-versioning/SKILL.md` | markdown | 355 | No |
| `skills/idea-refine/SKILL.md` | markdown | 178 | No |
| `skills/idea-refine/examples.md` | markdown | 238 | No |
| `skills/idea-refine/frameworks.md` | markdown | 99 | No |
| `skills/idea-refine/refinement-criteria.md` | markdown | 113 | No |
| `skills/idea-refine/scripts/idea-refine.sh` | shell | 15 | Yes |
| `skills/incremental-implementation/SKILL.md` | markdown | 249 | No |
| `skills/interview-me/SKILL.md` | markdown | 225 | No |
| `skills/observability-and-instrumentation/SKILL.md` | markdown | 203 | No |
| `skills/performance-optimization/SKILL.md` | markdown | 396 | No |
| `skills/planning-and-task-breakdown/SKILL.md` | markdown | 234 | No |
| `skills/security-and-hardening/SKILL.md` | markdown | 467 | No |
| `skills/shipping-and-launch/SKILL.md` | markdown | 310 | No |
| `skills/source-driven-development/SKILL.md` | markdown | 194 | No |
| `skills/spec-driven-development/SKILL.md` | markdown | 206 | No |
| `skills/test-driven-development/SKILL.md` | markdown | 398 | No |
| `skills/using-agent-skills/SKILL.md` | markdown | 191 | No |

## Issues (95)

### 🟡 MEDIUM: RP1

**Location:** `.claude/commands/webperf.md:10`  
**Confidence:** 70%  

**Message:** MCP server referenced without pinned version: 'npx lighthouse'.

**Remediation:** Pin the version: npx @scope/server@1.2.3

---

### 🟡 MEDIUM: RP1

**Location:** `.claude/commands/webperf.md:10`  
**Confidence:** 70%  

**Message:** MCP server referenced without pinned version: 'npx -p chrome-devtools-mcp'.

**Remediation:** Pin the version: npx @scope/server@1.2.3

---

### 🟡 MEDIUM: RP1

**Location:** `.claude/commands/webperf.md:15`  
**Confidence:** 70%  

**Message:** MCP server referenced without pinned version: 'npx -p chrome-devtools-mcp'.

**Remediation:** Pin the version: npx @scope/server@1.2.3

---

### 🟡 MEDIUM: RP1

**Location:** `.gemini/commands/webperf.toml:9`  
**Confidence:** 70%  

**Message:** MCP server referenced without pinned version: 'npx lighthouse'.

**Remediation:** Pin the version: npx @scope/server@1.2.3

---

### 🟡 MEDIUM: RP1

**Location:** `.gemini/commands/webperf.toml:9`  
**Confidence:** 70%  

**Message:** MCP server referenced without pinned version: 'npx -p chrome-devtools-mcp'.

**Remediation:** Pin the version: npx @scope/server@1.2.3

---

### 🟡 MEDIUM: RP1

**Location:** `.gemini/commands/webperf.toml:14`  
**Confidence:** 70%  

**Message:** MCP server referenced without pinned version: 'npx -p chrome-devtools-mcp'.

**Remediation:** Pin the version: npx @scope/server@1.2.3

---

### 🟡 MEDIUM: RP1

**Location:** `README.md:48`  
**Confidence:** 70%  

**Message:** MCP server referenced without pinned version: 'npx skills'.

**Remediation:** Pin the version: npx @scope/server@1.2.3

---

### 🟡 MEDIUM: RP1

**Location:** `README.md:49`  
**Confidence:** 70%  

**Message:** MCP server referenced without pinned version: 'npx skills'.

**Remediation:** Pin the version: npx @scope/server@1.2.3

---

### 🟡 MEDIUM: RP1

**Location:** `README.md:55`  
**Confidence:** 70%  

**Message:** MCP server referenced without pinned version: 'npx skills'.

**Remediation:** Pin the version: npx @scope/server@1.2.3

---

### 🟡 MEDIUM: RP1

**Location:** `README.md:56`  
**Confidence:** 70%  

**Message:** MCP server referenced without pinned version: 'npx skills'.

**Remediation:** Pin the version: npx @scope/server@1.2.3

---

### 🟡 MEDIUM: RP1

**Location:** `README.md:57`  
**Confidence:** 70%  

**Message:** MCP server referenced without pinned version: 'npx skills'.

**Remediation:** Pin the version: npx @scope/server@1.2.3

---

### 🟡 MEDIUM: RP1

**Location:** `agents/web-performance-auditor.md:20`  
**Confidence:** 70%  

**Message:** MCP server referenced without pinned version: 'npx lighthouse'.

**Remediation:** Pin the version: npx @scope/server@1.2.3

---

### 🟡 MEDIUM: RP1

**Location:** `agents/web-performance-auditor.md:20`  
**Confidence:** 70%  

**Message:** MCP server referenced without pinned version: 'npx -p chrome-devtools-mcp'.

**Remediation:** Pin the version: npx @scope/server@1.2.3

---

### 🟡 MEDIUM: RP1

**Location:** `agents/web-performance-auditor.md:25`  
**Confidence:** 70%  

**Message:** MCP server referenced without pinned version: 'npx -p chrome-devtools-mcp'.

**Remediation:** Pin the version: npx @scope/server@1.2.3

---

### 🟡 MEDIUM: RP1

**Location:** `agents/web-performance-auditor.md:37`  
**Confidence:** 70%  

**Message:** MCP server referenced without pinned version: 'npx -p chrome-devtools-mcp'.

**Remediation:** Pin the version: npx @scope/server@1.2.3

---

### 🟡 MEDIUM: RP1

**Location:** `commands/webperf.toml:9`  
**Confidence:** 70%  

**Message:** MCP server referenced without pinned version: 'npx lighthouse'.

**Remediation:** Pin the version: npx @scope/server@1.2.3

---

### 🟡 MEDIUM: RP1

**Location:** `commands/webperf.toml:9`  
**Confidence:** 70%  

**Message:** MCP server referenced without pinned version: 'npx -p chrome-devtools-mcp'.

**Remediation:** Pin the version: npx @scope/server@1.2.3

---

### 🟡 MEDIUM: RP1

**Location:** `commands/webperf.toml:14`  
**Confidence:** 70%  

**Message:** MCP server referenced without pinned version: 'npx -p chrome-devtools-mcp'.

**Remediation:** Pin the version: npx @scope/server@1.2.3

---

### 🟡 MEDIUM: RP1

**Location:** `docs/adoption-guide.md:30`  
**Confidence:** 70%  

**Message:** MCP server referenced without pinned version: 'npx skills'.

**Remediation:** Pin the version: npx @scope/server@1.2.3

---

### 🟡 MEDIUM: RP1

**Location:** `docs/comparison.md:26`  
**Confidence:** 70%  

**Message:** MCP server referenced without pinned version: 'npx skills'.

**Remediation:** Pin the version: npx @scope/server@1.2.3

---

### 🟡 MEDIUM: RP1

**Location:** `docs/comparison.md:26`  
**Confidence:** 70%  

**Message:** MCP server referenced without pinned version: 'npx skills'.

**Remediation:** Pin the version: npx @scope/server@1.2.3

---

### 🟡 MEDIUM: RP1

**Location:** `references/accessibility-checklist.md:127`  
**Confidence:** 70%  

**Message:** MCP server referenced without pinned version: 'npx axe-core'.

**Remediation:** Pin the version: npx @scope/server@1.2.3

---

### 🟡 MEDIUM: RP1

**Location:** `references/accessibility-checklist.md:128`  
**Confidence:** 70%  

**Message:** MCP server referenced without pinned version: 'npx pa11y'.

**Remediation:** Pin the version: npx @scope/server@1.2.3

---

### 🟡 MEDIUM: RP1

**Location:** `references/performance-checklist.md:121`  
**Confidence:** 70%  

**Message:** MCP server referenced without pinned version: 'npx webpack-bundle-analyzer'.

**Remediation:** Pin the version: npx @scope/server@1.2.3

---

### 🟡 MEDIUM: RP1

**Location:** `references/performance-checklist.md:123`  
**Confidence:** 70%  

**Message:** MCP server referenced without pinned version: 'npx vite-bundle-visualizer'.

**Remediation:** Pin the version: npx @scope/server@1.2.3

---

### 🟡 MEDIUM: RP1

**Location:** `references/performance-checklist.md:126`  
**Confidence:** 70%  

**Message:** MCP server referenced without pinned version: 'npx bundlesize'.

**Remediation:** Pin the version: npx @scope/server@1.2.3

---

### 🟡 MEDIUM: RP1

**Location:** `skills/browser-testing-with-devtools/SKILL.md:41`  
**Confidence:** 70%  

**Message:** MCP server referenced without pinned version: 'npx install'.

**Remediation:** Pin the version: npx @scope/server@1.2.3

---

### 🟡 MEDIUM: RP1

**Location:** `skills/ci-cd-and-automation/SKILL.md:88`  
**Confidence:** 70%  

**Message:** MCP server referenced without pinned version: 'npx tsc'.

**Remediation:** Pin the version: npx @scope/server@1.2.3

---

### 🟡 MEDIUM: RP1

**Location:** `skills/ci-cd-and-automation/SKILL.md:128`  
**Confidence:** 70%  

**Message:** MCP server referenced without pinned version: 'npx prisma'.

**Remediation:** Pin the version: npx @scope/server@1.2.3

---

### 🟡 MEDIUM: RP1

**Location:** `skills/ci-cd-and-automation/SKILL.md:152`  
**Confidence:** 70%  

**Message:** MCP server referenced without pinned version: 'npx playwright'.

**Remediation:** Pin the version: npx @scope/server@1.2.3

---

### 🟡 MEDIUM: RP1

**Location:** `skills/ci-cd-and-automation/SKILL.md:156`  
**Confidence:** 70%  

**Message:** MCP server referenced without pinned version: 'npx playwright'.

**Remediation:** Pin the version: npx @scope/server@1.2.3

---

### 🟡 MEDIUM: RP1

**Location:** `skills/ci-cd-and-automation/SKILL.md:207`  
**Confidence:** 70%  

**Message:** MCP server referenced without pinned version: 'npx vercel'.

**Remediation:** Pin the version: npx @scope/server@1.2.3

---

### 🟡 MEDIUM: RP1

**Location:** `skills/ci-cd-and-automation/SKILL.md:268`  
**Confidence:** 70%  

**Message:** MCP server referenced without pinned version: 'npx vercel'.

**Remediation:** Pin the version: npx @scope/server@1.2.3

---

### 🟡 MEDIUM: RP1

**Location:** `skills/ci-cd-and-automation/SKILL.md:348`  
**Confidence:** 70%  

**Message:** MCP server referenced without pinned version: 'npx tsc'.

**Remediation:** Pin the version: npx @scope/server@1.2.3

---

### 🟡 MEDIUM: RP1

**Location:** `skills/context-engineering/SKILL.md:55`  
**Confidence:** 70%  

**Message:** MCP server referenced without pinned version: 'npx tsc'.

**Remediation:** Pin the version: npx @scope/server@1.2.3

---

### 🟡 MEDIUM: RP1

**Location:** `skills/deprecation-and-migration/SKILL.md:91`  
**Confidence:** 70%  

**Message:** MCP server referenced without pinned version: 'npx migrate-check'.

**Remediation:** Pin the version: npx @scope/server@1.2.3

---

### 🟡 MEDIUM: RP1

**Location:** `skills/git-workflow-and-versioning/SKILL.md:229`  
**Confidence:** 70%  

**Message:** MCP server referenced without pinned version: 'npx tsc'.

**Remediation:** Pin the version: npx @scope/server@1.2.3

---

### 🟡 MEDIUM: RP1

**Location:** `skills/incremental-implementation/SKILL.md:206`  
**Confidence:** 70%  

**Message:** MCP server referenced without pinned version: 'npx tsc'.

**Remediation:** Pin the version: npx @scope/server@1.2.3

---

### 🟡 MEDIUM: RP1

**Location:** `skills/performance-optimization/SKILL.md:344`  
**Confidence:** 70%  

**Message:** MCP server referenced without pinned version: 'npx bundlesize'.

**Remediation:** Pin the version: npx @scope/server@1.2.3

---

### 🟡 MEDIUM: RP1

**Location:** `skills/performance-optimization/SKILL.md:347`  
**Confidence:** 70%  

**Message:** MCP server referenced without pinned version: 'npx lhci'.

**Remediation:** Pin the version: npx @scope/server@1.2.3

---

### 🟡 MEDIUM: RP1

**Location:** `skills/shipping-and-launch/SKILL.md:258`  
**Confidence:** 70%  

**Message:** MCP server referenced without pinned version: 'npx prisma'.

**Remediation:** Pin the version: npx @scope/server@1.2.3

---

### 🟡 MEDIUM: AS3

**Location:** `README.md:204`  
**Confidence:** 80%  

**Message:** Skill Enumeration

**Remediation:** Remove all code or instructions that list or read other skills' files or directories. Skills should operate independently; cross-skill access is a privilege escalation.

---

### 🟡 MEDIUM: AS3

**Location:** `README.md:210`  
**Confidence:** 80%  

**Message:** Skill Enumeration

**Remediation:** Remove all code or instructions that list or read other skills' files or directories. Skills should operate independently; cross-skill access is a privilege escalation.

---

### 🟡 MEDIUM: AS3

**Location:** `README.md:211`  
**Confidence:** 80%  

**Message:** Skill Enumeration

**Remediation:** Remove all code or instructions that list or read other skills' files or directories. Skills should operate independently; cross-skill access is a privilege escalation.

---

### 🟡 MEDIUM: AS3

**Location:** `README.md:212`  
**Confidence:** 80%  

**Message:** Skill Enumeration

**Remediation:** Remove all code or instructions that list or read other skills' files or directories. Skills should operate independently; cross-skill access is a privilege escalation.

---

### 🟡 MEDIUM: AS3

**Location:** `README.md:218`  
**Confidence:** 80%  

**Message:** Skill Enumeration

**Remediation:** Remove all code or instructions that list or read other skills' files or directories. Skills should operate independently; cross-skill access is a privilege escalation.

---

### 🟡 MEDIUM: AS3

**Location:** `README.md:236`  
**Confidence:** 80%  

**Message:** Skill Enumeration

**Remediation:** Remove all code or instructions that list or read other skills' files or directories. Skills should operate independently; cross-skill access is a privilege escalation.

---

### 🟡 MEDIUM: AS3

**Location:** `README.md:237`  
**Confidence:** 80%  

**Message:** Skill Enumeration

**Remediation:** Remove all code or instructions that list or read other skills' files or directories. Skills should operate independently; cross-skill access is a privilege escalation.

---

### 🟡 MEDIUM: AS3

**Location:** `README.md:243`  
**Confidence:** 80%  

**Message:** Skill Enumeration

**Remediation:** Remove all code or instructions that list or read other skills' files or directories. Skills should operate independently; cross-skill access is a privilege escalation.

---

### 🟡 MEDIUM: AS3

**Location:** `README.md:244`  
**Confidence:** 80%  

**Message:** Skill Enumeration

**Remediation:** Remove all code or instructions that list or read other skills' files or directories. Skills should operate independently; cross-skill access is a privilege escalation.

---

### 🟡 MEDIUM: AS3

**Location:** `README.md:245`  
**Confidence:** 80%  

**Message:** Skill Enumeration

**Remediation:** Remove all code or instructions that list or read other skills' files or directories. Skills should operate independently; cross-skill access is a privilege escalation.

---

### 🟡 MEDIUM: AS3

**Location:** `README.md:246`  
**Confidence:** 80%  

**Message:** Skill Enumeration

**Remediation:** Remove all code or instructions that list or read other skills' files or directories. Skills should operate independently; cross-skill access is a privilege escalation.

---

### 🟡 MEDIUM: AS3

**Location:** `agents/web-performance-auditor.md:176`  
**Confidence:** 80%  

**Message:** Skill Enumeration

**Remediation:** Remove all code or instructions that list or read other skills' files or directories. Skills should operate independently; cross-skill access is a privilege escalation.

---

### 🔴 HIGH: AS1

**Location:** `docs/codex-setup.md:13`  
**Confidence:** 27%  

**Message:** Agent Config Directory Access

**Remediation:** Remove all code or instructions that access agent configuration directories (.claude/, .codex/, .gemini/). If configuration values are needed, pass them explicitly as parameters or environment variables — never read the agent's own config files.

---

### 🔴 HIGH: AS1

**Location:** `docs/gemini-cli-setup.md:90`  
**Confidence:** 27%  

**Message:** Agent Config Directory Access

**Remediation:** Remove all code or instructions that access agent configuration directories (.claude/, .codex/, .gemini/). If configuration values are needed, pass them explicitly as parameters or environment variables — never read the agent's own config files.

---

### 🔴 HIGH: AS1

**Location:** `hooks/SDD-CACHE.md:97`  
**Confidence:** 85%  

**Message:** Agent Config Directory Access

**Remediation:** Remove all code or instructions that access agent configuration directories (.claude/, .codex/, .gemini/). If configuration values are needed, pass them explicitly as parameters or environment variables — never read the agent's own config files.

---

### 🟡 MEDIUM: AS3

**Location:** `hooks/SDD-CACHE.md:3`  
**Confidence:** 80%  

**Message:** Skill Enumeration

**Remediation:** Remove all code or instructions that list or read other skills' files or directories. Skills should operate independently; cross-skill access is a privilege escalation.

---

### 🟡 MEDIUM: AS3

**Location:** `skills/spec-driven-development/SKILL.md:169`  
**Confidence:** 80%  

**Message:** Skill Enumeration

**Remediation:** Remove all code or instructions that list or read other skills' files or directories. Skills should operate independently; cross-skill access is a privilege escalation.

---

### 🟡 MEDIUM: AS3

**Location:** `skills/spec-driven-development/SKILL.md:169`  
**Confidence:** 80%  

**Message:** Skill Enumeration

**Remediation:** Remove all code or instructions that list or read other skills' files or directories. Skills should operate independently; cross-skill access is a privilege escalation.

---

### 🟡 MEDIUM: AS3

**Location:** `skills/spec-driven-development/SKILL.md:169`  
**Confidence:** 80%  

**Message:** Skill Enumeration

**Remediation:** Remove all code or instructions that list or read other skills' files or directories. Skills should operate independently; cross-skill access is a privilege escalation.

---

### 🔴 HIGH: AR2

**Location:** `skills/shipping-and-launch/SKILL.md:25`  
**Confidence:** 80%  

**Message:** Anti-Refusal Statement

**Remediation:** Remove instructions that suppress warnings, disclaimers, or ethical commentary. Let the agent surface safety-relevant caveats to the user.

---

### 🟢 LOW: EA3

**Location:** `LICENSE:16`  
**Confidence:** 70%  

**Message:** Scope Creep

**Remediation:** Limit the skill's scope to its documented purpose. Remove instructions that enable the agent to perform actions outside its stated functionality.

---

### 🟢 LOW: EA3

**Location:** `skills/code-simplification/SKILL.md:103`  
**Confidence:** 75%  

**Message:** Scope Creep

**Remediation:** Limit the skill's scope to its documented purpose. Remove instructions that enable the agent to perform actions outside its stated functionality.

---

### 🟡 MEDIUM: EA2

**Location:** `skills/context-engineering/SKILL.md:66`  
**Confidence:** 75%  

**Message:** Autonomous Decision Making

**Remediation:** Add human-in-the-loop confirmation for destructive, irreversible, or high-impact operations. Never auto-execute commands that modify files, send data, or alter system state.

---

### 🟡 MEDIUM: EA2

**Location:** `skills/context-engineering/SKILL.md:280`  
**Confidence:** 75%  

**Message:** Autonomous Decision Making

**Remediation:** Add human-in-the-loop confirmation for destructive, irreversible, or high-impact operations. Never auto-execute commands that modify files, send data, or alter system state.

---

### 🟡 MEDIUM: EA2

**Location:** `skills/planning-and-task-breakdown/SKILL.md:216`  
**Confidence:** 75%  

**Message:** Autonomous Decision Making

**Remediation:** Add human-in-the-loop confirmation for destructive, irreversible, or high-impact operations. Never auto-execute commands that modify files, send data, or alter system state.

---

### 🟡 MEDIUM: EA2

**Location:** `skills/spec-driven-development/SKILL.md:80`  
**Confidence:** 75%  

**Message:** Autonomous Decision Making

**Remediation:** Add human-in-the-loop confirmation for destructive, irreversible, or high-impact operations. Never auto-execute commands that modify files, send data, or alter system state.

---

### 🟡 MEDIUM: EA2

**Location:** `skills/test-driven-development/SKILL.md:378`  
**Confidence:** 75%  

**Message:** Autonomous Decision Making

**Remediation:** Add human-in-the-loop confirmation for destructive, irreversible, or high-impact operations. Never auto-execute commands that modify files, send data, or alter system state.

---

### 🟡 MEDIUM: EA2

**Location:** `skills/using-agent-skills/SKILL.md:119`  
**Confidence:** 75%  

**Message:** Autonomous Decision Making

**Remediation:** Add human-in-the-loop confirmation for destructive, irreversible, or high-impact operations. Never auto-execute commands that modify files, send data, or alter system state.

---

### 🟡 MEDIUM: EA2

**Location:** `skills/using-agent-skills/SKILL.md:134`  
**Confidence:** 85%  

**Message:** Autonomous Decision Making

**Remediation:** Add human-in-the-loop confirmation for destructive, irreversible, or high-impact operations. Never auto-execute commands that modify files, send data, or alter system state.

---

### 🟡 MEDIUM: MP2

**Location:** `README.md:304`  
**Confidence:** 80%  

**Message:** Context Window Stuffing

**Remediation:** Implement context-window management that detects and rejects padding or stuffing attempts. Prioritize system instructions over user-injected content.

---

### 🔴 HIGH: PE3

**Location:** `skills/ci-cd-and-automation/SKILL.md:275`  
**Confidence:** 30%  

**Message:** Credential Access

**Remediation:** Remove references to credential paths. Use environment variables or secrets managers. For docs, use placeholder paths (e.g., /path/to/config). Never load .env or token files in production code paths.

---

### 🔴 HIGH: PE3

**Location:** `skills/context-engineering/SKILL.md:65`  
**Confidence:** 60%  

**Message:** Credential Access

**Remediation:** Remove references to credential paths. Use environment variables or secrets managers. For docs, use placeholder paths (e.g., /path/to/config). Never load .env or token files in production code paths.

---

### 🔴 HIGH: PE3

**Location:** `skills/security-and-hardening/SKILL.md:335`  
**Confidence:** 30%  

**Message:** Credential Access

**Remediation:** Remove references to credential paths. Use environment variables or secrets managers. For docs, use placeholder paths (e.g., /path/to/config). Never load .env or token files in production code paths.

---

### 🔴 HIGH: PE3

**Location:** `skills/security-and-hardening/SKILL.md:337`  
**Confidence:** 30%  

**Message:** Credential Access

**Remediation:** Remove references to credential paths. Use environment variables or secrets managers. For docs, use placeholder paths (e.g., /path/to/config). Never load .env or token files in production code paths.

---

### 🔴 HIGH: PE3

**Location:** `skills/security-and-hardening/SKILL.md:338`  
**Confidence:** 60%  

**Message:** Credential Access

**Remediation:** Remove references to credential paths. Use environment variables or secrets managers. For docs, use placeholder paths (e.g., /path/to/config). Never load .env or token files in production code paths.

---

### 🔴 HIGH: PE3

**Location:** `skills/security-and-hardening/SKILL.md:341`  
**Confidence:** 60%  

**Message:** Credential Access

**Remediation:** Remove references to credential paths. Use environment variables or secrets managers. For docs, use placeholder paths (e.g., /path/to/config). Never load .env or token files in production code paths.

---

### 🔴 HIGH: PE3

**Location:** `skills/security-and-hardening/SKILL.md:342`  
**Confidence:** 60%  

**Message:** Credential Access

**Remediation:** Remove references to credential paths. Use environment variables or secrets managers. For docs, use placeholder paths (e.g., /path/to/config). Never load .env or token files in production code paths.

---

### 🔴 HIGH: RA1

**Location:** `skills/code-simplification/SKILL.md:155`  
**Confidence:** 70%  

**Message:** Self-Modification

**Remediation:** Prevent the skill from modifying its own code, SKILL.md, or configuration files. Treat skill files as read-only at runtime.

---

### 🔴 HIGH: TM1

**Location:** `hooks/simplify-ignore-test.sh:51`  
**Confidence:** 95%  

**Message:** Tool Parameter Abuse

**Remediation:** Validate all tool parameters against an allowlist. Reject dangerous parameter values (shell=True, --force, -rf /) and use safe defaults.

---

### 🔴 HIGH: TM1

**Location:** `hooks/simplify-ignore-test.sh:79`  
**Confidence:** 95%  

**Message:** Tool Parameter Abuse

**Remediation:** Validate all tool parameters against an allowlist. Reject dangerous parameter values (shell=True, --force, -rf /) and use safe defaults.

---

### 🔴 HIGH: TM1

**Location:** `hooks/simplify-ignore-test.sh:103`  
**Confidence:** 95%  

**Message:** Tool Parameter Abuse

**Remediation:** Validate all tool parameters against an allowlist. Reject dangerous parameter values (shell=True, --force, -rf /) and use safe defaults.

---

### 🔴 HIGH: TM1

**Location:** `hooks/simplify-ignore-test.sh:130`  
**Confidence:** 95%  

**Message:** Tool Parameter Abuse

**Remediation:** Validate all tool parameters against an allowlist. Reject dangerous parameter values (shell=True, --force, -rf /) and use safe defaults.

---

### 🔴 HIGH: TM1

**Location:** `hooks/simplify-ignore-test.sh:151`  
**Confidence:** 95%  

**Message:** Tool Parameter Abuse

**Remediation:** Validate all tool parameters against an allowlist. Reject dangerous parameter values (shell=True, --force, -rf /) and use safe defaults.

---

### 🔴 HIGH: TM1

**Location:** `hooks/simplify-ignore-test.sh:167`  
**Confidence:** 95%  

**Message:** Tool Parameter Abuse

**Remediation:** Validate all tool parameters against an allowlist. Reject dangerous parameter values (shell=True, --force, -rf /) and use safe defaults.

---

### 🔴 HIGH: TM1

**Location:** `hooks/simplify-ignore-test.sh:183`  
**Confidence:** 95%  

**Message:** Tool Parameter Abuse

**Remediation:** Validate all tool parameters against an allowlist. Reject dangerous parameter values (shell=True, --force, -rf /) and use safe defaults.

---

### 🔴 HIGH: TM1

**Location:** `hooks/simplify-ignore-test.sh:200`  
**Confidence:** 95%  

**Message:** Tool Parameter Abuse

**Remediation:** Validate all tool parameters against an allowlist. Reject dangerous parameter values (shell=True, --force, -rf /) and use safe defaults.

---

### 🔴 HIGH: TM1

**Location:** `hooks/simplify-ignore-test.sh:219`  
**Confidence:** 95%  

**Message:** Tool Parameter Abuse

**Remediation:** Validate all tool parameters against an allowlist. Reject dangerous parameter values (shell=True, --force, -rf /) and use safe defaults.

---

### 🔴 HIGH: TM1

**Location:** `hooks/simplify-ignore.sh:62`  
**Confidence:** 95%  

**Message:** Tool Parameter Abuse

**Remediation:** Validate all tool parameters against an allowlist. Reject dangerous parameter values (shell=True, --force, -rf /) and use safe defaults.

---

### 🔴 HIGH: TM2

**Location:** `hooks/simplify-ignore.sh:138`  
**Confidence:** 75%  

**Message:** Chaining Abuse

**Remediation:** Limit tool chaining depth and validate the output of each tool before passing it to the next. Require explicit user approval for multi-step chains.

---

### 🔴 HIGH: TM2

**Location:** `hooks/simplify-ignore.sh:270`  
**Confidence:** 75%  

**Message:** Chaining Abuse

**Remediation:** Limit tool chaining depth and validate the output of each tool before passing it to the next. Require explicit user approval for multi-step chains.

---

### 🔴 HIGH: TM1

**Location:** `skills/api-and-interface-design/SKILL.md:165`  
**Confidence:** 80%  

**Message:** Tool Parameter Abuse

**Remediation:** Validate all tool parameters against an allowlist. Reject dangerous parameter values (shell=True, --force, -rf /) and use safe defaults.

---

### 🔴 HIGH: YR4

**Location:** `skills/browser-testing-with-devtools/SKILL.md:288`  
**Confidence:** 80%  

**Message:** YARA rule 'agent_skill_prompt_injection_hidden_instructions': Prompt injection or hidden instructions embedded in AI agent skill text [agent_skills]

**Remediation:** Remove offensive tool references and exploit code. Legitimate agent skills should not contain penetration testing tools, exploit frameworks, or reconnaissance utilities.

---

### 🔴 HIGH: YR1

**Location:** `skills/browser-testing-with-devtools/SKILL.md:64`  
**Confidence:** 75%  

**Message:** YARA rule 'info_stealer': Information stealer patterns (credential harvesting, browser data theft) [malware]

**Remediation:** Remove the malware payload or compromised file entirely. Investigate how it entered the skill and audit all other artifacts for additional indicators of compromise.

---

### 🔴 HIGH: YR4

**Location:** `skills/security-and-hardening/SKILL.md:21`  
**Confidence:** 80%  

**Message:** YARA rule 'agent_skill_prompt_injection_hidden_instructions': Prompt injection or hidden instructions embedded in AI agent skill text [agent_skills]

**Remediation:** Remove offensive tool references and exploit code. Legitimate agent skills should not contain penetration testing tools, exploit frameworks, or reconnaissance utilities.

---

## Inspection Completeness

| Metric | Value |
|--------|-------|
| Execution | successful |
| Coverage | 100.0% |
| Fully inspected | 174 |
| Partially inspected | 0 |
| Entirely uninspected | 0 |

### Scope Exclusions

| Reason / Status | Location | Details |
|-----------------|----------|---------|
| excluded_directory | `.git/` | Directory tree is excluded from the configured scan scope. |
| hidden_file | `.gitattributes` | Hidden file is excluded from the configured scan scope. |
| hidden_file | `.gitignore` | Hidden file is excluded from the configured scan scope. |

### Analyzer Statuses

| Reason / Status | Location | Details |
|-----------------|----------|---------|
| completed | `` |  |
| completed | `` |  |
| manifest_absent | `` | No compatible manifest was present for this analyzer. |
| completed | `` |  |
| manifest_absent | `` | No compatible manifest was present for this analyzer. |
| disabled_by_configuration | `` | Analyzer was disabled by the requested configuration. |
| disabled_by_configuration | `` | Analyzer was disabled by the requested configuration. |
| disabled_by_configuration | `` | Analyzer was disabled by the requested configuration. |
| disabled_by_configuration | `` | Analyzer was disabled by the requested configuration. |
| completed | `` |  |
| completed | `` |  |
| completed | `` |  |
| completed | `` |  |
| completed | `` |  |
| completed | `` |  |
| completed | `` |  |
| completed | `` |  |
| completed | `` |  |
| completed | `` |  |
| completed | `` |  |
| completed | `` |  |
| completed | `` |  |
| completed | `` |  |
| completed | `` |  |

### Limitations

- Analyzer was disabled by the requested configuration.
- Analyzer was disabled by the requested configuration.
- Analyzer was disabled by the requested configuration.
- Analyzer was disabled by the requested configuration.

## Metadata

- **Executable Scripts:** Yes

*Generated by SkillSpector v2.5.0*