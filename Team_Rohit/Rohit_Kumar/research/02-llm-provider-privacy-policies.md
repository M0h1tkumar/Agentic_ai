# Privacy Policies of Major LLM Providers (OpenAI, Google, Claude)

## Introduction

Privacy is an important consideration when using Large Language Models (LLMs). Different providers have different policies regarding data collection, model training, data retention, human review, and enterprise security.

The three providers discussed in this document are:

- OpenAI
- Google Gemini
- Anthropic Claude

The privacy rules can differ significantly between **consumer products** and **business/API products**.

---

## Comparison

| Feature | OpenAI | Google (Gemini) | Claude (Anthropic) |
|---------|---------|----------------|-------------------|
| Consumer Data May Be Used for Improvement | Yes, depending on settings | Yes, depending on product/settings | Depends on product and user controls |
| Business/API Data Used for Training by Default | No | Generally subject to product/contract terms | Commercial products have separate protections |
| Human Review | Possible in specific situations | Some interactions may be reviewed | Depends on product and situation |
| Data Controls | Available | Available | Available |
| Enterprise Products | Yes | Yes | Yes |
| Data Encryption | Yes | Yes | Yes |

---

## OpenAI

OpenAI provides consumer products such as ChatGPT and developer products through the OpenAI API.

For business products and the API, OpenAI states that customer inputs and outputs are **not used to train models by default**. Organizations can explicitly opt in to sharing certain data for model improvement. ([OpenAI Business Data](https://openai.com/business-data/))

For personal ChatGPT accounts, users can control whether new conversations are used to improve models through the **"Improve the model for everyone"** setting. Temporary Chats are not used to train models and are handled separately. ([OpenAI Data Controls](https://help.openai.com/en/articles/7730893-data-controls-faq))

### Strengths

- Business and API data is not used for training by default
- Data control settings are available
- Enterprise privacy and security controls
- Retention controls are available for certain business products
- Encryption is used for business data

### Considerations

- Consumer and business policies are different
- Personal users should review their Data Controls settings
- Data handling depends on the specific OpenAI product being used

---

## Google Gemini

Google provides Gemini for both consumers and organizations.

Google states that Gemini data can be used to improve its generative AI services, depending on the product and applicable settings.

Google also states that a subset of certain Gemini interactions can be reviewed by human reviewers to improve services and maintain safety. ([Google Gemini Privacy Documentation](https://support.google.com/gemini/answer/16836988))

Users can manage Gemini activity and related data settings through their Google Account.

### Strengths

- Enterprise and Google Workspace privacy controls
- Strong cloud security infrastructure
- User activity and privacy controls
- Integration with Google Cloud and Workspace

### Considerations

- Some consumer interactions can be used to improve services
- Some interactions may be reviewed by human reviewers
- Users should check Gemini Activity and privacy settings
- Confidential information should not be shared without understanding the applicable policy

---

## Claude (Anthropic)

Anthropic provides Claude through consumer products and commercial/API services.

Anthropic separates consumer and commercial data handling, so the exact policy depends on which Claude product is being used.

Commercial customers receive separate contractual and data-handling protections from consumer users.

### Strengths

- Separate commercial and consumer data policies
- Strong focus on privacy and AI safety
- API and enterprise controls
- Business customers receive additional contractual protections

### Considerations

- Consumer and commercial policies are different
- Data-use rules can depend on user settings and product type
- Users should review the policy for the exact Claude service they are using

---

## Consumer vs Enterprise

One of the most important privacy differences is whether an organization is using a consumer AI product or a business/API product.

### Consumer AI

Examples:

- ChatGPT Free/Plus/Pro
- Gemini consumer applications
- Claude consumer plans

Consumer services can have different rules regarding:

- Model improvement
- Data retention
- Human review
- User data controls

### Enterprise / API

Business products generally provide additional controls for organizations, such as:

- Access management
- Data retention controls
- Security controls
- Contractual privacy commitments
- Different rules for model training

---

## Important Privacy Risks

Users should avoid sending highly sensitive information to AI systems unless the applicable privacy and security controls have been verified.

Examples include:

- Passwords
- API keys
- Private encryption keys
- Bank information
- Confidential source code
- Customer databases
- Personal identification documents
- Proprietary company information

---

## Best Practices

### 1. Minimize Data

Only send the information that is necessary for the task.

### 2. Use Business/API Products for Sensitive Work

Organizations should prefer products with clear enterprise privacy commitments.

### 3. Check Training Settings

Review whether conversations or feedback can be used to improve the provider's models.

### 4. Check Retention Policies

Understand how long data may be stored and whether deletion controls are available.

### 5. Avoid Sharing Secrets

Never place passwords, private keys, or other credentials into an LLM prompt.

### 6. Review Human-Access Policies

Understand whether interactions may be reviewed by human reviewers.

---

## Conclusion

OpenAI, Google, and Anthropic all provide privacy and security controls, but their policies are **not identical**.

The most important distinction is between consumer and business/API products.

OpenAI states that business and API data is not used to train models by default. Google documents that some Gemini interactions can be reviewed by human reviewers and that data may be used to improve its services depending on the product and settings. Anthropic also maintains separate consumer and commercial data policies.

Therefore, users should not judge privacy based only on the provider's name. They should check the **specific product, account type, settings, retention policy, and training policy** before sharing sensitive information.

---

## References

- OpenAI — Business Data Privacy: https://openai.com/business-data/
- OpenAI — Data Controls: https://help.openai.com/en/articles/7730893-data-controls-faq
- Google — Gemini Privacy and Activity Controls: https://support.google.com/gemini/
- Google — Gemini Connected Apps and Privacy: https://support.google.com/gemini/answer/16836988
- Anthropic — Privacy Center: https://privacy.anthropic.com/