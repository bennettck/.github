from aws_cdk import (
    Stack,
    CfnOutput,
    aws_iam as iam,
)
from constructs import Construct


class GitHubOidcStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # GitHub OIDC provider
        github_provider = iam.OpenIdConnectProvider(
            self,
            "GitHubOidcProvider",
            url="https://token.actions.githubusercontent.com",
            client_ids=["sts.amazonaws.com"],
            thumbprints=["ffffffffffffffffffffffffffffffffffffffff"],
        )

        # Trust policy for GitHub Actions from specific repos/branches
        github_principal = iam.OpenIdConnectPrincipal(
            github_provider,
            conditions={
                "StringEquals": {
                    "token.actions.githubusercontent.com:aud": "sts.amazonaws.com",
                },
                "StringLike": {
                    "token.actions.githubusercontent.com:sub": [
                        "repo:bennettck/collections:*",
                        "repo:bennettck/kcr:*",
                    ],
                },
            },
        )

        # IAM role for GitHub Actions
        deploy_role = iam.Role(
            self,
            "GitHubActionsDeployRole",
            role_name="github-actions-cdk-deploy",
            assumed_by=github_principal,
            description="Role assumed by GitHub Actions for CDK deployments",
        )

        # CloudFormation permissions
        deploy_role.add_to_policy(
            iam.PolicyStatement(
                sid="CloudFormation",
                effect=iam.Effect.ALLOW,
                actions=[
                    "cloudformation:*",
                ],
                resources=["*"],
            )
        )

        # Lambda permissions
        deploy_role.add_to_policy(
            iam.PolicyStatement(
                sid="Lambda",
                effect=iam.Effect.ALLOW,
                actions=[
                    "lambda:*",
                ],
                resources=["*"],
            )
        )

        # API Gateway permissions
        deploy_role.add_to_policy(
            iam.PolicyStatement(
                sid="ApiGateway",
                effect=iam.Effect.ALLOW,
                actions=[
                    "apigateway:*",
                ],
                resources=["*"],
            )
        )

        # S3 permissions
        deploy_role.add_to_policy(
            iam.PolicyStatement(
                sid="S3",
                effect=iam.Effect.ALLOW,
                actions=[
                    "s3:*",
                ],
                resources=["*"],
            )
        )

        # IAM permissions (for role/policy management)
        deploy_role.add_to_policy(
            iam.PolicyStatement(
                sid="IAM",
                effect=iam.Effect.ALLOW,
                actions=[
                    "iam:*",
                ],
                resources=["*"],
            )
        )

        # CloudWatch permissions
        deploy_role.add_to_policy(
            iam.PolicyStatement(
                sid="CloudWatch",
                effect=iam.Effect.ALLOW,
                actions=[
                    "cloudwatch:*",
                    "logs:*",
                ],
                resources=["*"],
            )
        )

        # EventBridge permissions
        deploy_role.add_to_policy(
            iam.PolicyStatement(
                sid="EventBridge",
                effect=iam.Effect.ALLOW,
                actions=[
                    "events:*",
                    "scheduler:*",
                ],
                resources=["*"],
            )
        )

        # SNS permissions
        deploy_role.add_to_policy(
            iam.PolicyStatement(
                sid="SNS",
                effect=iam.Effect.ALLOW,
                actions=[
                    "sns:*",
                ],
                resources=["*"],
            )
        )

        # RDS permissions
        deploy_role.add_to_policy(
            iam.PolicyStatement(
                sid="RDS",
                effect=iam.Effect.ALLOW,
                actions=[
                    "rds:*",
                ],
                resources=["*"],
            )
        )

        # EC2 and VPC permissions
        deploy_role.add_to_policy(
            iam.PolicyStatement(
                sid="EC2VPC",
                effect=iam.Effect.ALLOW,
                actions=[
                    "ec2:*",
                ],
                resources=["*"],
            )
        )

        # Secrets Manager permissions
        deploy_role.add_to_policy(
            iam.PolicyStatement(
                sid="SecretsManager",
                effect=iam.Effect.ALLOW,
                actions=[
                    "secretsmanager:*",
                ],
                resources=["*"],
            )
        )

        # SSM permissions
        deploy_role.add_to_policy(
            iam.PolicyStatement(
                sid="SSM",
                effect=iam.Effect.ALLOW,
                actions=[
                    "ssm:*",
                ],
                resources=["*"],
            )
        )

        # CDK bootstrap permissions (for asset publishing)
        deploy_role.add_to_policy(
            iam.PolicyStatement(
                sid="CDKBootstrap",
                effect=iam.Effect.ALLOW,
                actions=[
                    "ecr:*",
                    "ssm:GetParameter",
                ],
                resources=["*"],
            )
        )

        # STS permissions (for CDK)
        deploy_role.add_to_policy(
            iam.PolicyStatement(
                sid="STS",
                effect=iam.Effect.ALLOW,
                actions=[
                    "sts:AssumeRole",
                ],
                resources=["arn:aws:iam::*:role/cdk-*"],
            )
        )

        # Output the role ARN
        CfnOutput(
            self,
            "DeployRoleArn",
            value=deploy_role.role_arn,
            description="ARN of the GitHub Actions deploy role - add this to GitHub secrets as AWS_DEPLOY_ROLE_ARN",
            export_name="GitHubActionsDeployRoleArn",
        )
