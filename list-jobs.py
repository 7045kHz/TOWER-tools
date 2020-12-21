#!/usr/bin/env python3

import os
import json
import requests
from requests.auth import HTTPBasicAuth


USER=os.environ.get("TOWER_USER")
PASSWORD=os.environ.get("TOWER_PASSWORD")
TOWER_PAGE_SIZE=int(os.environ.get("TOWER_PAGE_SIZE",10))
TOWER=os.environ.get("TOWER_HOST")
TOWER_TEMP_DIR=os.environ.get("TOWER_TEMP_DIR")
if len(TOWER)  < 1 or len(USER)  < 1 or len(PASSWORD)<8:
  print("")
  print("Exiting - User Must Setup Environmental Variables first")
  print("")
  print("Example File: cat $HOME/.ansible")
  print("")
  print("  export TOWER_HOST=https://registry.rsyslab.com")
  print("  export TOWER_USER=your_account")
  print("  export TOWER_PASSWORD=your_password")
  print("  export TOWER_TEMP_DIR=$HOME/.tower")
  print("  export TOWER_PAGE_SIZE=30")
  print("  [[ -d  $TOWER_TEMP_DIR ]] || mkdir -p $TOWER_TEMP_DIR")
  print("")
  print("Then source .ansible prior to running command")
  exit()



jobs_temp_file = "{}/jobs.json".format(TOWER_TEMP_DIR)

if os.path.exists(jobs_temp_file):
  os.remove(jobs_temp_file)

r=requests.post("{}/api/v2/jobs?order_by=-started&page_size={}".format(TOWER,TOWER_PAGE_SIZE), auth=HTTPBasicAuth(USER, PASSWORD))
h=r.text

j=open(jobs_temp_file,'w')
j.write(str(h))
j.close()

f=open(jobs_temp_file,'r')
data=json.load(f)


name=""
jid=""
playbook=""
started=""
status=""

print("%10s %30s %30s %30s %30s" % ("Job ID","Name","Playbook","Started","Status"))
print("%10s %30s %30s %30s %30s" % ("==========", "==============================","==============================","==============================","===================="))
for i in data['results']:
  for x in i:
    if x == "id":
      jid=str(i[x])
    if x == "name":
      name=str(i[x])
    if x == "playbook":
      playbook=str(i[x])
    if x ==  "started":
      started=str(i[x])
    if x ==  "status":
      status=str(i[x])
    if x ==  "webhook_service" and len(name) > 1 and len(playbook) > 1 and len(started) > 1 and len(status) > 1:
      print("%10s %30s %30s %30s %30s" % (jid,name,playbook,started,status))


f.close()
