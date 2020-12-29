##############################################################
#
# iam_stack.py
#
# Resources:
#   Lambda Execution Role
#
# Exports:
#  lambda_execution_role_arn
#
##############################################################

from aws_cdk import (
  aws_iam as iam,
  core
)

class IAMStack(core.Stack):

  def __init__(self, scope: core.Construct, construct_id: str, env, **kwargs) -> None:
    super().__init__(scope, construct_id, **kwargs)

    # get acct id for policies
    acct_id=env['account']

    # create lambda execution role
    self._defcon_lambda_role=iam.Role(self,"Defcon Lambda Role",
      role_name="Defcon_Lambda_Execution_Role",
      assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
      # update the resources later
      inline_policies=[
        iam.PolicyDocument(
          statements=[iam.PolicyStatement(
            actions=["sns:Publish"],
            effect=iam.Effect.ALLOW,
            resources=["arn:aws:sns:us-east-1:"+acct_id+":remediator-topic","arn:aws:sns:us-east-1:"+acct_id+":DatadogSNSTopic"]
          )],
        ),
        iam.PolicyDocument(
          statements=[iam.PolicyStatement(
            actions=["iam:AttachGroupPolicy","iam:AttachUserPolicy","iam:AttachRolePolicy",
                     "iam:DetachGroupPolicy","iam:DetachUserPolicy","iam:DetachRolePolicy"
                    ],
            effect=iam.Effect.ALLOW,
            resources=["*"],
            conditions={
              "ArnEqualsIfExists": {
                "iam:PolicyARN": "arn:aws:iam::"+acct_id+":policy/bleu_team_deny_all"
              }
            }
          )]
      )],
      managed_policies=[
        iam.ManagedPolicy.from_aws_managed_policy_name('IAMReadOnlyAccess'),
        iam.ManagedPolicy.from_aws_managed_policy_name('service-role/AWSLambdaBasicExecutionRole')  
      ]
    )

  # Exports
  @property
  def defcon_lambda_role(self) -> iam.IRole:
    return self._defcon_lambda_role
