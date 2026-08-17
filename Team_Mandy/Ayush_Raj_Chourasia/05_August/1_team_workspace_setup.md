# Setting Up Team Workspaces in Multica

In Multica, workspaces are logical boundaries that separate agents, knowledge bases, and team members. 

## 1. Creation
- Navigate to the **Admin Dashboard** in Multica.
- Click **Create Workspace** and assign it a name (e.g., `Team_Mandy_Workspace`).

## 2. Resource Allocation
- You can allocate specific computational quotas (e.g., max API tokens per day) to the workspace to prevent cost overruns.
- Assign dedicated RAG collections (from AnythingLLM) exclusively to this workspace so that other teams cannot query your private datasets.

## 3. User Onboarding
- Invite team members via their emails.
- Assign roles: `Admin` (can modify agents and skills) or `Viewer` (can only chat with agents).
