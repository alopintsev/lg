import json
import sys
def save_config(conf):  
  old_conf = load_config(True)
  print(old_conf)
  #preserve old passwords if new is not in save request
  if not conf['admin_password']:
    conf["admin_password"] = old_conf["admin_password"]
  if not conf['password']:
    conf["password"] = old_conf["password"]

  file = open('instance/config.json','w')
  file.write(json.dumps(conf))
  file.close
  return True

def load_config(full=False):
  data = {}
  try:      
    with open("instance/config.json", "r") as read_file:
      data = json.load(read_file)
      
      if not full:
        if 'password' in data.keys() and data['password']:
            data['isPasswordExist'] = True
            data.pop('password', None)
        if 'admin_password' in data.keys() and data['admin_password']:
            data['isAdminPasswordExist'] = True
            data.pop('admin_password', None)

    read_file.close()
  except:
    e = sys.exc_info()[0]
    print("Exception while open config file")    
    data["Exception"] = str(e)
  return data
  