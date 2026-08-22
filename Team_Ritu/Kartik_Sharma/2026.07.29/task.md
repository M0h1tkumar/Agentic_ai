

---

# 1. Top 5 Benefits and Limitations of Developing AI Agents in GitHub Copilot

## Benefits

### 1. Built into VS Code
GitHub Copilot works directly inside VS Code, allowing developers to write, test, and manage AI agents without switching between multiple tools.

### 2. AI-Assisted Coding
It provides code suggestions, completes functions, and helps identify errors, making development faster and more efficient.

### 3. Better Code Understanding
Copilot can explain existing code, making it easier to understand large projects and onboard new developers.

### 4. Increased Productivity
It automates repetitive coding tasks, allowing developers to focus more on solving problems and designing features.

### 5. Seamless GitHub Integration
Copilot integrates well with GitHub repositories, making commits, pull requests, and collaboration easier.

---

## Limitations

### 1. Requires Internet Connection
Most AI features rely on cloud services, so a stable internet connection is usually needed.

### 2. Limited Project Context
Copilot may not fully understand the complete project or business requirements, leading to incorrect suggestions.

### 3. Human Review is Necessary
Generated code should always be reviewed for correctness, security, and performance.

### 4. Paid Subscription
Many advanced Copilot features require a paid subscription.

### 5. Privacy Concerns
Organizations handling sensitive code may have concerns about sharing code with cloud-based AI services.

---

# 2. Session-Based Authentication vs Token-Based Authentication

## Session-Based Authentication

### Advantages

- Stores session information securely on the server.
- Users can be logged out instantly by destroying the session.
- Simple to implement for traditional web applications.
- Sensitive user data is not stored on the client.
- Suitable for applications that maintain user state.

### Limitations

- Uses server memory to store session data.
- Scaling across multiple servers is more complex.
- Less suitable for REST APIs and mobile applications.
- Sessions can expire after inactivity.
- Every request requires the server to verify the session.

---

## Token-Based Authentication

### Advantages

- Stateless authentication with no server-side session storage.
- Ideal for REST APIs, mobile apps, and microservices.
- Easy to scale across multiple servers.
- Supports Single Sign-On (SSO) and distributed systems.
- Better suited for modern cloud-based applications.

### Limitations

- Stolen tokens can be used until they expire.
- Revoking tokens before expiration is more difficult.
- Tokens must be stored securely on the client.
- Token refresh and expiration management adds complexity.
- Incorrect implementation can create security risks.
