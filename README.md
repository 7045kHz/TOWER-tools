# TOWER-tools
Basic toolkit for CLI based job monitoring, and running.

## Setup Environmental Variables
Replace values with those of your environment and source file.

```
$ cat example.env
export TOWER_HOST=https://tower.example.com
export TOWER_USER=user
export TOWER_PASSWORD=password
export TOWER_TEMP_DIR=$HOME/.tower
export TOWER_PAGE_SIZE=30
[[ -d $TOWER_TEMP_DIR ]]  ||  mkdir -p $TOWER_TEMP_DIR

$ source example.env
```
## List Jobs
Default is the last 30 based on all organizations that you are a member of.

```
$ ./list-jobs.py 
    Job ID                           Name                       Playbook                        Started                         Status
========== ============================== ============================== ==============================           ====================
      3042                     commandRun                 commandRun.yml    2020-12-20T23:22:34.051541Z                     successful
      3041                     commandRun                 commandRun.yml    2020-12-20T23:22:09.115032Z                     successful
[-cut-]

```
### List Jobs Help
Currently none - planning on allowing drilldown by organization.

## Monitor Job
Displays the standard output of a Job.
```
$  ./monitor.py -j 3011
Identity added: /tmp/awx_3011_odke14c3/artifacts/3011/ssh_key_data (ansible@tower.example.com)
SSH password: 

PLAY [Create User John Doe] ****************************************************

TASK [Gathering Facts] *********************************************************
[WARNING]: Platform linux on host ns1.rsyslab.com is using the discovered
Python interpreter at /usr/bin/python, but future installation of another
Python interpreter could change this. See https://docs.ansible.com/ansible/2.9/
reference_appendices/interpreter_discovery.html for more information.
ok: [ns1.rsyslab.com]
ok: [api.rsyslab.com]

TASK [Ensure group "johndoe" exists] *******************************************
ok: [ns1.rsyslab.com]
ok: [api.rsyslab.com]

TASK [Add the user 'johndoe' with a bash shell, appending the group 'johndoe' to the user's groups] ***
ok: [ns1.rsyslab.com]
ok: [api.rsyslab.com]

PLAY RECAP *********************************************************************
api.rsyslab.com            : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
ns1.rsyslab.com            : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
$

```
### Monitor Help
```
$ ./monitor.py -h
usage: monitor.py [-h] [-V] [-j JOB_ID]

monitor.py monitors the stdout output from Ansible Tower Jobs.

optional arguments:
  -h, --help            show this help message and exit
  -V, --version         show program version
  -j JOB_ID, --job_id JOB_ID
                        Job ID to monitor

```
## List Inventories

```
$ ./list-inventories.py 
Inventory ID                           Name Orgainization
============ ==============================   ========
         1                 Demo Inventory          1
         4           pi_dynamic_inventory          2
         5       hyperv_dynamic_inventory          2
         6         p330_dynamic_inventory          2
         7                          Tower          2

```
### List Inventories Help
Currently none - planning on allowing drilldown by organization.

## List Templates
```
Template ID                           Name                                 Playbook                                 Modified 
=========== ==============================           ==============================           ============================== 
         22                     commandRun                           commandRun.yml              2020-12-20T19:58:57.606265Z
         21                       cat_file                             cat_file.yml              2020-11-22T00:16:15.164141Z
         20                       Fdisk -l                                fdisk.yml              2020-11-21T02:20:56.799444Z
         19            Distribute SSH Keys                 distribute_user_keys.yml              2020-11-20T15:04:19.574773Z
         18                 add_basic_user                       add_basic_user.yml              2020-11-19T01:08:17.005386Z
         17         Add_Basic_JohnDoe_User               add_basic_johndoe_user.yml              2020-11-19T00:57:15.357299Z
         13                    Hello World                          hello-world.yml              2020-11-18T02:29:17.671784Z
          7              Demo Job Template                          hello_world.yml              2020-11-15T02:53:01.717711Z
 
```
### List Templates Help
Currently none - planning on allowing drilldown by organization.

## Start Template
```
```
### Start Template Help
Generic Help
```
$ ./start-template.py -h
usage: start-template.py [-h] [-V] [-f JSON_FILE] [-t TEMPLATE_ID] [-g]

start-template.py starts an Asible Tower Job through the commandRun.yml
template.

optional arguments:
  -h, --help            show this help message and exit
  -V, --version         show program version
  -f JSON_FILE, --json_file JSON_FILE
                        JSON file with extra_vars
  -t TEMPLATE_ID, --template_id TEMPLATE_ID
                        Numeric Template ID (see list-templates.py)
  -g, --generate        Generates a basic JSON Job File to stdout


```
## Walkthrough

Create JSON for adding Survey Answers, identifying Inventories, template and adding extra_vars values to a template.
```
$  ./list-inventories.py
Inventory ID                           Name Orgainization
============ ==============================   ========
         1                 Demo Inventory          1
         4           pi_dynamic_inventory          2
         5       hyperv_dynamic_inventory          2
         6         p330_dynamic_inventory          2
         7                          Tower          2

$ ./list-templates.py 
Template ID                           Name                                 Playbook                                 Modified 
=========== ==============================           ==============================           ============================== 
         22                     commandRun                           commandRun.yml              2020-12-20T19:58:57.606265Z
         21                       cat_file                             cat_file.yml              2020-11-22T00:16:15.164141Z
         20                       Fdisk -l                                fdisk.yml              2020-11-21T02:20:56.799444Z
         19            Distribute SSH Keys                 distribute_user_keys.yml              2020-11-20T15:04:19.574773Z
         18                 add_basic_user                       add_basic_user.yml              2020-11-19T01:08:17.005386Z
         17         Add_Basic_JohnDoe_User               add_basic_johndoe_user.yml              2020-11-19T00:57:15.357299Z
         13                    Hello World                          hello-world.yml              2020-11-18T02:29:17.671784Z
          7              Demo Job Template                          hello_world.yml              2020-11-15T02:53:01.717711Z

$ ./start-template.py -g >template.json

$ vi template.json
{
    "inventory":4,
    "extra_vars": {}
}


$ ./start-template.py -t 13 -f template.json 
Job Started Successfully

$ ./list-jobs.py 
    Job ID                           Name                       Playbook                        Started                         Status
========== ============================== ============================== ==============================           ====================
      3046                    Hello World                hello-world.yml    2020-12-21T17:20:32.135486Z                     successful
      3045                     commandRun                 commandRun.yml    2020-12-21T17:17:08.681907Z                     successful
      3042                     commandRun                 commandRun.yml    2020-12-20T23:22:34.051541Z                     successful


$ ./monitor.py -j 3046
Identity added: /tmp/awx_3047__xsaymgx/artifacts/3047/ssh_key_data (ansible@tower.example.com)
SSH password: 

PLAY [Hello World!] ************************************************************

TASK [Gathering Facts] *********************************************************
[WARNING]: Platform linux on host ns1.example.com is using the discovered
Python interpreter at /usr/bin/python, but future installation of another
Python interpreter could change this. See https://docs.ansible.com/ansible/2.9/
reference_appendices/interpreter_discovery.html for more information.
ok: [host1.example.com]
ok: [host2.example.com]

TASK [Hello World!] ************************************************************
changed: [host1.example.com]
changed: [host2.example.com]

PLAY RECAP *********************************************************************
host1.example.com            : ok=2    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
host2.example.com            : ok=2    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   





```

# MIT license
```
MIT License

Copyright (c) [year] [fullname]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
