#!/usr/bin/env python3

import os
import json
import requests
from requests.auth import HTTPBasicAuth
import urllib3
urllib3.disable_warnings()

USER=os.environ.get("TOWER_USER","")
PASSWORD=os.environ.get("TOWER_PASSWORD","")
TOWER_PAGE_SIZE=int(os.environ.get("TOWER_PAGE_SIZE",10))
TOWER=os.environ.get("TOWER_HOST","")
TOWER_TEMP_DIR=os.environ.get("TOWER_TEMP_DIR","")
if len(TOWER)  < 1 or len(USER)  < 1 or len(PASSWORD)<8:
  print("")
  print("Exiting - User Must Setup Environmental Variables first")
  print("")
  print("Example File: cat $HOME/.ansible")
  print("")
  print("  export TOWER_HOST=https://tower.example.com")
  print("  export TOWER_USER=your_account")
  print("  export TOWER_PASSWORD=your_password")
  print("  export TOWER_TEMP_DIR=$HOME/.tower")
  print("  export TOWER_PAGE_SIZE=30")
  print("  [[ -d  $TOWER_TEMP_DIR ]] || mkdir -p $TOWER_TEMP_DIR")
  print("")
  print("Then source .ansible prior to running command")
  exit()



templates_temp_file = "{}/templates.json".format(TOWER_TEMP_DIR)

if os.path.exists(templates_temp_file):
  os.remove(templates_temp_file)


r=requests.post("{}/api/v2/job_templates?order_by=-created&page_size={}".format(TOWER,TOWER_PAGE_SIZE), auth=HTTPBasicAuth(USER, PASSWORD),verify=False)
h=r.text


j=open(templates_temp_file,'w')
j.write(str(h))
j.close()

f=open(templates_temp_file,'r')
data=json.load(f)


name=""
tid=""
playbook=""
modified=""

print("%10s %30s %40s %40s " % ("Template ID","Name","Playbook","Modified"))
print("%10s %30s %40s %40s " % ("===========", "==============================","==============================","=============================="))
for (i) in data['results']:
  for x in i: 
    #print("x = ",x," = ", i[x])
    if x == "id":
      tid=str(i[x])
    if x == "name":
      name=str(i[x])
    if x == "playbook":
      playbook=str(i[x])
    if x ==  "modified":
      modified=str(i[x])
    if x ==  "webhook_service" and len(name) > 1 and len(playbook) > 1 and len(modified) > 1 :
      print("%11s %30s %40s %40s" % (tid,name,playbook,modified))


f.close()
