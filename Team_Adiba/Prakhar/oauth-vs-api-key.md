# OAuth vs API Keys

## What’s the Difference?

Whenever an application wants to talk to an API, the API needs some way to know **who is making the request and whether they are allowed to make it**.

Two common ways to handle this are **OAuth** and **API keys**.

They can look similar because both involve sending some kind of credential with an API request, but they are meant for different situations.

A simple way to think about it is:

* **OAuth** → “Let this application access my account with these permissions.”
* **API Key** → “This application is allowed to use this API.”

---

# OAuth

OAuth becomes useful when an application needs to access something that belongs to a **user**.

For example, imagine an app that wants to access your Google Drive. You don't want to give that app your Google password. Instead, you authorize it through Google's login system and give it permission to access your Drive.

The app then receives an **access token** that it can use to make authorized requests.

### Why OAuth is Useful

There are several reasons OAuth is commonly used for user-based applications:

* Access tokens can be **short-lived**, which limits the damage if one gets exposed.
* You can use **scopes** to control exactly what the application can access.
* Users never have to hand over their actual password to the application.
* It supports **delegated authorization**, meaning you're giving an application permission to act on your behalf.
* **Refresh tokens** can be used to obtain new access tokens without making the user log in every time.
* Different users can have different permissions depending on what they have authorized.

### What's the Catch?

OAuth is powerful, but it isn't exactly simple.

There are authorization flows to implement, tokens to manage, expiration to handle, scopes to configure, and sometimes refresh tokens to deal with as well.

So if you're building a small server-to-server API and there isn't a user involved, setting up OAuth may be more complexity than you actually need.

---

# API Keys

API keys are much simpler.

Imagine you've built a weather API and you want to know which application is making requests to it. You can give that application an API key and require it to include the key whenever it calls your API.

For example:

```http
GET /weather?city=Bhubaneswar
Authorization: ApiKey YOUR_API_KEY
```

The API checks the key and decides whether the request should be allowed.

There is no user sitting in front of the application approving access. The key is simply being used as a credential for the application.

### Why API Keys Are Popular

The biggest advantage is **simplicity**.

* They're easy to create and use.
* They're straightforward to include in API requests.
* They work well for server-to-server communication.
* There's no interactive login or authorization flow.
* They're relatively easy to understand and manage.
* Development is usually much simpler than implementing OAuth.

### But There Is a Security Trade-off

The simplicity of API keys also comes with some risks.

If someone gets hold of your API key, they may be able to use it until you **revoke or rotate** the key.

API keys also generally don't provide the same level of fine-grained permissions that OAuth scopes can provide. They don't naturally represent a user's consent either.

That's why API keys should be treated like **secrets**. They shouldn't be hard-coded into public repositories or exposed in client-side code when they provide access to protected resources.

Long-lived API keys are especially risky because a stolen key can remain useful for a long time.

---

# OAuth vs API Key

Here's a quick way to compare them:

| Feature              | **OAuth**                                    | **API Key**                               |
| -------------------- | -------------------------------------------- | ----------------------------------------- |
| **What is used?**    | Usually an access token                      | API key                                   |
| **Typical lifetime** | Often temporary                              | Usually stays valid until revoked/rotated |
| **Main purpose**     | Delegated authorization                      | Application/client authentication         |
| **User involvement** | ✅ Supports user authorization                | ❌ Usually no user consent flow            |
| **Permissions**      | ✅ Can use detailed scopes                    | Usually more coarse-grained               |
| **If leaked**        | Short-lived/scoped tokens can limit exposure | Can be risky if the key remains valid     |
| **Revocation**       | Tokens/authorization can be revoked          | Key can be revoked or rotated             |
| **Refresh**          | Refresh tokens can obtain new access tokens  | Usually requires generating a new key     |
| **Complexity**       | Higher                                       | Low                                       |
| **Best suited for**  | User-facing apps and third-party access      | Simple APIs and server-to-server calls    |

---

# So, Which One Should You Use?

The easiest way to decide is to ask **one question**:

### Is a user giving your application permission to access their data?

If **yes**, OAuth is usually the better choice.

For example:

* “Let this app access my Google Drive.”
* “Allow this application to read my GitHub repositories.”
* “Connect my Microsoft account to this application.”
* “Sign in with Google.”

These situations involve **user authorization**, which is where OAuth makes sense.

### What if there isn't a user involved?

If your application simply needs to communicate with another service, an API key may be enough.

For example:

* Your application calling a weather API.
* A backend calling a maps API.
* A service calling a translation API.
* One internal service communicating with another.

In these cases, you may not need the complexity of an OAuth authorization flow.

---

# The Easy Way to Remember

Think about the difference like this:

> **OAuth:** “I give this application permission to access my resources, and I decide what it can access.”

> **API Key:** “This application has a credential that allows it to call this API.”

So, **OAuth is mainly about delegated access and permissions**, while **API keys are generally a simpler way to identify and authenticate an application or client**.
