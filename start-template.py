#!/usr/bin/env python3

import os
import json
import requests
from requests.auth import HTTPBasicAuth
import argparse

# Define the program description
desc = 'start-template.py starts an Asible Tower Job through the commandRun.yml template.'

# Initiate the parser with a description
parser = argparse.ArgumentParser(description=desc)
parser.add_argument("-V", "--version", help="show program version", action="store_true")
parser.add_argument("-f", "--json_file", help="JSON file with extra_vars")
parser.add_argument("-t", "--template_id", help="Numeric Template ID (see list-templates.py)")
parser.add_argument("-g", "--generate", help="Generates a basic JSON Job File to stdout", action="store_true")

args=parser.parse_args()

if args.version:
  print("start-template.py Version 1.0")
  exit()

if args.generate:

  print('{')
  print('    "inventory":4,')
  print('    "extra_vars": {}')
  print('}')
  exit()

if args.json_file:
  if os.path.exists(args.json_file):
    json_job_file=args.json_file
  else:
    print(args.json_file + " does not exist. exiting")
    exit(1)
else: 
  print("Must provide a JSON job file and Template ID")
  print("For more details:  start-template.py -h")
  exit(1)

if args.template_id:
  TEMPLATE_ID=args.template_id


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


headers={'Content-Type':'application/json'}
if os.path.exists(json_job_file):
  r=requests.post("{}/api/v2/job_templates/{}/launch/".format(TOWER,TEMPLATE_ID), data=open(json_job_file,'rb'),auth=HTTPBasicAuth(USER, PASSWORD),headers=headers)

if r.status_code == 201:
  print("Job Started Successfully")


