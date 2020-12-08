#!flask/bin/python
from flask import Flask, jsonify, request, session, redirect
from flask import render_template

from mod_aaa import controllers as aaa
from mod_config import controllers as conf

import ciscomasscmd

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('config.py')

app.secret_key = app.config['SECRET_KEY']

# index page
@app.route('/', methods = ['GET'])
def index():
#    aaa.validate_request()
    configFile = conf.load_config(False)
    return render_template("index.html", showAdminLinkMenu = True, appSettings = configFile)

# access login page
@app.route('/login', methods = ['GET'])
def login():    
    fromUrl = request.args.get('from', '/')
    return render_template("login.html", fromUrl=fromUrl)

# access admin page
@app.route('/admin', methods = ['GET'])
def admin():
    if(aaa.isAuthorized()):
        configFile = conf.load_config()        
        return render_template("admin.html", appSettings = configFile)
    else:
        return redirect("/login?from=admin", 302)


# ---=== REST methods ===---

# Check authorization
@app.route('/api/v1/authorize', methods = ['POST'])
def restAuthorize():        
    instanceConf = conf.load_config(True)
    content = request.get_json(force=True)    
    if(instanceConf['admin_password'] == content['key']):
        session['isAuthorized'] = True
        return "{authorized:true}"
    else:
        return 'Unauthorized', 404

# Save configuration
@app.route('/api/v1/config', methods = ['POST'])
def saveConfig():
    if(not aaa.isAuthorized()):
        return 'Unauthorized', 404
    content = request.get_json(force=True)    
    conf.save_config(content)
    return {'saved':'ok'}

# Get configuration
@app.route('/api/v1/config', methods = ['GET'])
def readConfig():
    if(not aaa.isAuthorized()):
        return 'Unauthorized', 404
    content = conf.load_config()
    return content

# Logout
@app.route('/api/v1/logout', methods = ['POST'])
def restLogout():
    session.pop('isAuthorized', None)
    return "{logout:true}"


# Execute commands on devices
@app.route('/api/v1/command/execute', methods = ['POST'])
def command():    
    instanceConfig = conf.load_config(True)
    #if validation failed - send Bad Request
    if(aaa.validate_request() == False):
      return 'Incorrect request', 400
    content = request.get_json(force=True)
    print(content)
    resp = ciscomasscmd.go( instanceConfig['login'],
                            instanceConfig['password'],
                            content['hosts'],
                            content['commands'])
    return resp

if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'],
            host=app.config['BIND_HOST'],
            port=app.config['BIND_PORT'])

