from flask import current_app, request, session
from mod_config import controllers as conf

def validate_request():  
    content = request.get_json(force=True)
    instanceConf = conf.load_config(False)

    numOfHosts = len(content['hosts'])
    numOfCommands = len(content['commands'])

    if(numOfHosts == 0 or numOfHosts > 3):
      return False

    if(numOfCommands == 0 or numOfCommands >3):
      return False

    #check if all commands in request allowed
    for cmd in content['commands']:
      if cmd not in instanceConf['commands']:
        return False

    #check if all hosts in request allowed
    for host in content['hosts']:
      if host not in instanceConf['hosts']:
        return False

 
    return True

def isAuthorized():
  rule =  request.url_rule
  #check authorization only for  /admin URL
  if not 'admin' in rule.rule and not 'config' in rule.rule:
    return True    
  #for admin access check that session exists
  return 'isAuthorized' in session
  