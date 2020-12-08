#!flask/bin/python

import napalm
import sys
import os
import re
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed

DEBUG = 1

def go(user, password, devices, commands):
  resp = ''
  if DEBUG: print("Found devices:", devices)
  if DEBUG: print("Found commands:", commands)  
  with ThreadPoolExecutor(max_workers = 4) as executor:
    future_to_res = {executor.submit(exec_commands, user, password, device, commands): device for device in devices}
    for future in as_completed(future_to_res):
        try:
            data = future.result()            
        except Exception as exc:
            resp += "Exception:" + str(exc)            
        else:
            resp += data
  return resp

def exec_commands(user, password, dev_name, commands):
  #return if nothing to do  
  if len(dev_name) == 0 or len(commands) == 0:
    return
  driver = napalm.get_network_driver('ios')
  output = ""
  #througout all devices and execute all command per device
  try:
    output += "--==  " + dev_name + " ==--\n"
    try:
      dev = driver(dev_name, user, password)
      dev.open()
      try:
        for cmd in commands:
          if DEBUG: print("->", cmd);
          output += "->" + cmd + "\n"
          out = dev.device.send_command_expect(cmd, "#")
          if DEBUG: print("<-", out)
          output += "<-" + out + "\n"
      except:
        output += "Exception, cannot execute cmd:" + cmd + "\n"
        print("Exception, cannot execute cmd:", cmd)
      dev.close()
    except:
        output += "Exception, cannot connect to:" + dev_name + "\n"
        print("Exception, cannot connect to:", dev_name)
  except:
    output += "Something goes wrong" + "\n"
    print("Something goes wrong")
  #print(output)
  return output


