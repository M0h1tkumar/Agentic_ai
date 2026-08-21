# OAuth vs API Key

## Overview

**OAuth** and **API Keys** are two commonly used approaches for authenticating applications when they access APIs.
OAuth is generally used when an application needs to access resources **on behalf of a user**, while API keys are commonly used when an application simply needs to **identify and authenticate itself to an API**.

# OAuth

## Advantages

* More secure for user-based applications
* Access tokens can be short-lived
* Supports scopes, allowing limited permissions
* Users don’t need to give an application their password
* Supports delegated authorization
* Tokens can be refreshed without asking the user to log in again
* Useful when multiple users need different permissions

## Disadvantages

* More complex to implement
* Requires authorization flows
* Requires handling access tokens, refresh tokens, expiration, scopes, etc.
* More components are involved compared with an API key
* Can be overkill for simple server-to-server APIs

# API Key

## Advantages

* Very simple to implement
* Easy to send with API requests
* Good for server-to-server communication
* Easy to understand and manage for simple APIs
* Doesn’t require an interactive user authorization flow
* Lower development complexity

## Disadvantages

* If leaked, an attacker may be able to use it until it is revoked or rotated
* Usually provides less granular authorization than OAuth scopes
* Doesn’t naturally represent a specific user’s consent
* Requires proper secret management
* Long-lived keys increase the impact of credential leakage


# Comparison Table

| Feature | **OAuth** | **API Key** |
|---|---|---|
| **Credential type** | Dynamic access token | Static credential |
| **Lifetime** | Usually temporary; can expire | Usually long-lived until revoked/rotated |
| **Authentication** | Token-based authorization | Key-based authentication |
| **User authorization** | ✅ Supports delegated user authorization | ❌ Usually doesn't represent delegated user consent |
| **Permissions / scopes** | ✅ Fine-grained scopes possible | Usually more coarse-grained |
| **Security if leaked** | Better if short-lived + scoped | Riskier because key may remain valid |
| **Revocation** | Can revoke tokens/authorization | Key can be revoked, but usually requires key management |
| **Token refresh** | Can use refresh tokens | Usually requires generating/replacing the key |
| **Implementation complexity** | Higher | Low |
| **Setup** | More complicated | Very simple |
| **Best for** | User-facing apps and third-party access | Server-to-server/API access |
| **Example** | “Allow this app to access my Google Drive” | “Use this API key to call my weather API” |

# Conclusion

## When to Use OAuth

Use **OAuth** when:
> **A user is granting your application access to their account/data.**
Examples:
- Login with Google
- Access user's Google Drive
- Access user's GitHub repositories
- Access user's Microsoft account

## When to Use an API Key

Use an **API key** when: 
> **Your application simply needs to authenticate itself to an API.**
Examples:
- Weather API
- Maps API
- Translation API
- Internal service-to-service API


### In One Line

> **OAuth = “Let this application access my resources with these permissions.”**
> **API Key = “This application is allowed to call this API.”**