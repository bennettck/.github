#!/usr/bin/env python3
import aws_cdk as cdk

from github_oidc_stack import GitHubOidcStack

app = cdk.App()

GitHubOidcStack(
    app,
    "github-oidc",
    env=cdk.Environment(region="us-east-1"),
)

app.synth()
