# defcon-cdk

## Lockdown your AWS Account

Howto Install:  
If needed, export your AWS profile:  
`export AWS_PROFILE=profile_name`

Create a virtual environment and launch the stacks:  
```
python3 -m venv .venv  
source .venv/bin/activate   
python3 -m pip install -r requirements.txt  
cdk bootstrap aws://<account-id>/<region>  
cdk synth   
cdk deploy all
```

Enable or disable defcon lockdown through the lambda interface in the console with a test event.

Ex.
```
{ "defcon_level": 1 }
```

(c) Copyright 2020 - NickTheSecurityDude

Disclaimer:  
For informational/educational purposes only.  Bugs are likely and can be reported on github.  
Using this will incur AWS charges.
