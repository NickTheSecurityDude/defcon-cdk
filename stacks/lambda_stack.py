##############################################################
#
# lambda_stack.py
#
# Resources:
#  1 lambda functions (code in /lambda folder (from_asset))
#
##############################################################

from aws_cdk import (
  aws_iam as iam,
  aws_lambda as lambda_,
  core
)

class LambdaStack(core.Stack):

  def __init__(self, scope: core.Construct, construct_id: str, defcon_lambda_role: iam.IRole, env, **kwargs) -> None:
    super().__init__(scope, construct_id, **kwargs)

    # get acct id for policies
    acct_id=env['account']

    # create the Event DefCon Lambda function
    self._iam_event_checker_func=lambda_.Function(self,"DefCon Lambda Func",
      code=lambda_.Code.from_asset("lambda/"),
      handler="DefCon.lambda_handler",
      runtime=lambda_.Runtime.PYTHON_3_8,
      role=defcon_lambda_role,
      timeout=core.Duration.seconds(60)                                            
    )


