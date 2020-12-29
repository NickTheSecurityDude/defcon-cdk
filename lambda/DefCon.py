import boto3
import json
import time
#import yaml

#this will skip for any defcon actions (lock as well as unlock)
white_users=['']
white_roles=['Remediator_Lambda_Execution_Role','Defcon_Lambda_Execution_Role']

def do_defcon(defcon,acct_id):
  client = boto3.client('iam')

  deny_policy_arn="arn:aws:iam::"+acct_id+":policy/bleu_team_deny_all"

  if defcon == 1:
    action="locked"
  elif defcon==5:
    action="unlocked"
  else:
    print("defcon level not valid.  Use int not string")
    return 1

  #do users
  print(action+" users")
  users = client.list_users()['Users']
  for user in users:
    username=user['UserName']
    if username not in white_users:
      if defcon==1:
        response = client.attach_user_policy(
          UserName=username,
          PolicyArn=deny_policy_arn
        )
      elif defcon==5:
        try:
          response = client.detach_user_policy(
            UserName=username,
            PolicyArn=deny_policy_arn
          )
        except:
          print("Policy not attached or IAM error")
          pass
      print(username+ " "+action)
    else:
      print("Skipping user: "+username+" whitelisted")

  # do roles
  roles = client.list_roles()['Roles']
  for role in roles:
    rolename=role['RoleName']
    role_arn=role['Arn']
    #print(role_arn)
    if "role/aws-service-role/" in role_arn or "datadog-" in role_arn or "DatadogIntegrationRole" in role_arn:
      print("Skipping service role: "+rolename)
    elif rolename not in white_roles:
      if defcon==1:
        response = client.attach_role_policy(
          RoleName=rolename,
          PolicyArn=deny_policy_arn
        )
      elif defcon==5:
        try:
          response = client.detach_role_policy(
            RoleName=rolename,
            PolicyArn=deny_policy_arn
          )
        except:
          print("Policy not attached or iam error")
          pass
      print(rolename+" "+action)
    else:
      print("Skipping role: "+rolename+" whitelisted")

  return 1

def lambda_handler(event, context):
  # Pass the defcon_level in the event
  # defcon_level 1 = lock down all users and roles (add deny policy)
  # defcon_level 5 = unlock all users and roles (removes deny policy even if
  #   it was denied before defcon 1)
  #
  # ex.
  #
  # { "defcon_level": 1 }
  #
  # Add appropriate access to this before running, remove after running
  # ensure this function and the deny policy have not been modified
  # limited to first 1000 results, skips service roles
  # for informational use only, may contain bugs, do not use in production

  acct_id=context.invoked_function_arn.split(":")[4]

  defcon=0

  try:
    event['defcon_level']
  except:
    print("You must pass defcon_level in the event")
    return 0

  if event['defcon_level'] == 1:
    print("Defcon 1, lock down!!!")
    defcon=1
  else:
    print("Defcon 5, all clear!!!")
    defcon=5

  do_defcon(defcon,acct_id)

  print("(HIGH) Defcon Level: "+str(defcon)+" initiated")
  print("NEW SECURITY EVENT!!!",event)

  return "Completed"
