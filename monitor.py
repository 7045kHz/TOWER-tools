#!/usr/bin/env python3

import os
import json
import requests
from requests.auth import HTTPBasicAuth
import argparse
import urllib3
urllib3.disable_warnings()

# Define the program description
desc = 'monitor.py monitors the stdout output from Ansible Tower Jobs.'

# Initiate the parser with a description
parser = argparse.ArgumentParser(description=desc)
parser.add_argument("-V", "--version", help="show program version", action="store_true")
parser.add_argument("-j", "--job_id", help="Job ID to monitor")

args=parser.parse_args()

if args.version:
  print("monitor.py Version 1.0")
  exit()

if args.job_id:
  JOB_ID=args.job_id

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

json_job_file='example.json'

headers={'Content-Type':'application/json'}
if os.path.exists(json_job_file):
  r=requests.get("{}/api/v2/jobs/{}/stdout/?format=ansi".format(TOWER,JOB_ID), auth=HTTPBasicAuth(USER, PASSWORD),headers=headers,verify=False)
  print(r.text)



