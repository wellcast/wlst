##
#  WLST Script to configure Weblogic managed servers with coherence arguments for ATG SQL Repository cache
#
##

import time
from time import gmtime, strftime, localtime
#from java.util.regex import *
#from weblogic.management.runtime import ExecuteThread
import sys
import getopt

domain="test_coherence"
scriptdir="/u02/oracle/script"
domainconfigfile=domain+"_configfile.secure"
domainkeyfile=domain+"_keyfile.secure"
url="t3://172.16.70.190:7001"
logfile=scriptdir+"/logs/"+domain+"_"+strftime("%d%b%Y%H%M%S", localtime())+".log"

def usage():
    print "Usage:"
    print "domain_collect.wlst [config_file.secure] [key_file.secure] [t3://admin_url] [server_argumets_file]"

def openSession():
    if connected != 'true' :
       try:
         connect(userConfigFile=domainconfigfile, userKeyFile=domainkeyfile, url=url)
       except WLSTException,e:
         print 'Error description: ', e
         sys.exit(0)

def getDomainName():
    openSession()
    domainConfig()
    cd ('/')
    return cmo.getName()

def getManagedServers():
    openSession()
    serverConfig()
    return cmo.getServers()

def getAdminServerName():
    openSession()
    domainConfig()
    return cmo.getAdminServerName()

def editMode():
    edit()
    startEdit()

def editActivate():
    save()
    activate(block="true")

def readCfgFile(flpath):
    f = open(flpath)
    lines = f.read().splitlines()
    cfgarray = {}
    for l in lines:
        #cfgarray[l.split()[0]] = l.split()[1]
        al = l.split(';')
        cfgarray[al[0]] = al[1]
    return cfgarray

def setMSsStartArgumets(wlsargs):
    print "Starting weblogic server start configuration..."
    openSession()
    sstartargs=readCfgFile(wlsargs)
    servers=getManagedServers()
    adminsrvname=getAdminServerName()
    editMode()
    for s in servers:
        if s.getName() != adminsrvname:
            cd('/Servers/'+s.getName()+'/ServerStart/'+s.getName())
            print "Managed Server: "+s.getName()
            print "Current Args: "+get('Arguments')
            print "New Args: "+sstartargs[s.getName()]
            set('Arguments',sstartargs[s.getName()])

if __name__== "main":
   print "##"
   print "## Log file: "+logfile
   print "##"
   redirect(logfile,'true')
   sys.stdout = open(logfile,"w")
   argc = len(sys.argv)
   if argc != 5 :
     usage()
     sys.exit(0)
   domainconfigfile=sys.argv[1]
   domainkeyfile=sys.argv[2]
   url=sys.argv[3]
   serverstartcfg=sys.argv[4]
   setMSsStartArgumets(serverstartcfg)
