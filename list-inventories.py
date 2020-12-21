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



inventories_temp_file = "{}/inventories.json".format(TOWER_TEMP_DIR)

if os.path.exists(inventories_temp_file):
  os.remove(inventories_temp_file)

r=requests.post("{}/api/v2/inventories?order_by=id&page_size={}".format(TOWER,TOWER_PAGE_SIZE), auth=HTTPBasicAuth(USER, PASSWORD))
h=r.text


j=open(inventories_temp_file,'w')
j.write(str(h))
j.close()

f=open(inventories_temp_file,'r')
data=json.load(f)


name=""
iid=""
orgainization=""

print("%10s %30s %10s" % ("Inventory ID","Name","Orgainization"))
print("%10s %30s %10s" % ("============", "==============================","========"))
for i in data['results']:
  for x in i:
    #print(x, " = ",  str(i[x]))
    if x == "id":
      iid=str(i[x])
    if x == "name":
      name=str(i[x])
    if x == "organization":
      organization=str(i[x])
    if x ==  "pending_deletion" and len(name) > 1 and len(organization) > 0 :
      print("%10s %30s %10s" % (iid,name,organization))


f.close()
