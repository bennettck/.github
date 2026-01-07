# GitHub OIDC Stack

This is a standalone CDK app that creates the AWS IAM resources needed for GitHub Actions to deploy CDK stacks via OIDC authentication.

## What it creates

- **OIDC Identity Provider** - Trusts GitHub's token issuer (`token.actions.githubusercontent.com`)
- **IAM Role** - `github-actions-cdk-deploy` role that GitHub Actions can assume
- **Trust Policy** - Scoped to `main` branch of `bennettck/collections` and `bennettck/kcr` repos

## One-time deployment

This stack should be deployed manually once, before setting up the GitHub Actions workflows.

```bash
cd infra/github-oidc
pip install -r requirements.txt
cdk deploy
```

## After deployment

1. Copy the `DeployRoleArn` output value from the deployment
2. Add it as a secret to both repos:
   - Go to repo → Settings → Secrets and variables → Actions
   - Add repository secret:
     - Name: `AWS_DEPLOY_ROLE_ARN`
     - Value: (the ARN from step 1)

## Important notes

- This stack is intentionally **separate** from the main CDK app
- Running `cdk deploy --all` in the main `infra/` directory will NOT touch this stack
- Changes to `infra/github-oidc/` will NOT trigger the automated deploy workflow

## Modifying trusted repos

To allow additional repos to assume this role, edit `github_oidc_stack.py` and add entries to the `StringLike` condition:

```python
"token.actions.githubusercontent.com:sub": [
    "repo:bennettck/collections:ref:refs/heads/main",
    "repo:bennettck/kcr:ref:refs/heads/main",
    "repo:bennettck/new-repo:ref:refs/heads/main",  # Add new repos here
],
```

Then redeploy manually:

```bash
cd infra/github-oidc
cdk deploy
```
