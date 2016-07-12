#!/usr/bin/python

# README-FIRST
#
# This script lists different IPs attached to one or more machines on interface bond1.
# If you want IPs from other interface change bond1 to appropriate value (ex. eth0)
# Make sure paramiko is installed as the user running this script
#      sudo pip install paramiko
# It assumes that each host machine is enabled for SSO (or any common user name/pwd across all machines). You will be asked to provide your SSO creds.
# Usage:  list-ips.sh <host-details.csv>
#          Structure of host-details.csv- First line must be header.
#             host,ip
#             my-host.mydomain.com, 10.148.9.35
#
# @author: Kulki


import paramiko
import sys
import csv
import getpass

def getIPs(host, user, pwd):

   client = paramiko.SSHClient()
   client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
   client.connect(host, username=user, password=pwd, timeout=3)
   stdin, stdout, stderr = client.exec_command("sudo ip addr show dev bond1 |grep inet | awk '{print $2'}")
   ret = "";

   for line in stdout:
      ret +=line.strip('\n')
      ret += ', '
   client.close()
   return ret

if (len(sys.argv) < 1):
   print '<script-name> <csv-file>'
   print 'The csv file should contain headers as <host,ip>'
   sys.exit(1)

# Get Password
print 'Enter your SSO id and password'
user = raw_input('SSO id: ')
pword = getpass.getpass()

allips = {}
with open(sys.argv[1]) as csvfile:
   reader = csv.DictReader(csvfile)
   for row in reader:
   #   print 'Connecting to '+ row['host']
     try:
       # attIps = getIPs(row['ip'], row['user'], row['pwd'])
        attIps = getIPs(row['ip'], user, pword)
        allips[row['host']] = attIps
        print '' + row['host'] + '   :   ' + attIps
     except paramiko.ssh_exception.AuthenticationException:
        print ''+ row['host']  + '   :   Invalid Credentials'
     except:
        print ''+ row['host']  + '   :   Unknown error'

