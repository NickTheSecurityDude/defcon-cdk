#!/usr/bin/env python3

###################################################################
#
# 0. Prerequisite (for the policy)
#   - remediator-cdk
#
# 1. IAM Stack

# 2. Lambda Stack
#   - DefCon.py
# 
###################################################################

from aws_cdk import core

import boto3
import sys

client = boto3.client('sts')
# region is always us-east-1 for this
region=client.meta.region_name

if region != 'us-east-1':
  print("This app may only be run from us-east-1")
  sys.exit()

account_id = client.get_caller_identity()["Account"]

my_env = {'region': 'us-east-1', 'account': account_id}

from stacks.iam_stack import IAMStack
from stacks.lambda_stack import LambdaStack

proj_name="defcon-demo-"

app = core.App()

iam_stack=IAMStack(app,proj_name+"iam",env=my_env)
lambda_stack=LambdaStack(app, proj_name+"lambda",defcon_lambda_role=iam_stack.defcon_lambda_role,env=my_env)

app.synth()
