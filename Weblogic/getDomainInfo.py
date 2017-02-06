#!/bin/bash
export LC_ALL=en_US.ISO-8859-1
domainconfigfile="/opt/scripts/oracle/wlst/wls_configfile.secure"
domainkeyfile="/opt/scripts/oracle/wlst/wls_keyfile.secure"
emailsmtp=":25"
emailfrom=""
emailto=""
#emailto="danilo.fantinato@accurate.com.br"
emailsubjectprefix="Collect "
case $1 in
  domain_a)
      echo "Collecting domain "
      logfile="-`date +'%Y%m%d-%H%M-%s'`.txt"
      admin="t3://wls:15000"

  ;;
  domain_b)
      echo "Collecting domain "
      logfile="-`date +'%Y%m%d-%H%M-%s'`.txt"
      admin="t3://wls:16000"
  ;;
  *)
      echo "Usage: $0 domain_a|domain_b"
      exit
  ;;
esac
/opt/oracle/fmw/wlserver_10.3/common/bin/wlst.sh /opt/scripts/oracle/wlst/domain_collect.wlst $domainconfigfile $domainkeyfile $admin >/tmp/$logfile 2>&1
/bin/gzip /tmp/$logfile
/usr/bin/uuencode /tmp/$logfile.gz $logfile.gz | /bin/mailx -S smtp="$emailsmtp" -s "$emailsubjectprefix $1 `date +'%Y%m%d-%H%M'`"  -r "$emailfrom" $emailto
rm -f /tmp/$logfile.gz

# Jython para monitoracao de weblogic
import time
from time import gmtime, strftime, localtime
from java.util.regex import *
from weblogic.management.runtime import ExecuteThread
import sys
import getopt

def usage():
    print "Usage:"
    print "domain_collect.wlst [-c config_file.secure] [-k key_file.secure]"

def openSession():
    if connected != 'true' :
       try:
         connect(userConfigFile=uconfigfile, userKeyFile=ukeyfile, url=url)
       except WLSTException,e:
         print 'Error description: ', e
         sys.exit(0)

def getRunningServerNames():
    openSession()
    domainConfig()
    return cmo.getServers()

def getDomainName():
    openSession()
    domainRuntime()
    cd ('/')
    return cmo.getName()

def monitorThreads():
    serverNames = getRunningServerNames()
    domainRuntime()

    print '**************************************************************'
    print '************* Domain: ', getDomainName()
    print '************* Monitor ThreadPoolRuntime **********************'
    print '************* Collect Date: ',strftime("%a, %d %b %Y %H:%M:%S", localtime())
    print '**************************************************************'
    for name in serverNames:
      try:
        print '  -> Server Name: ', name.getName()
        cd('/ServerServices/'+name.getName()+'/RuntimeService/ServerRuntime/'+name.getName()+'/ThreadPoolRuntime/ThreadPoolRuntime')
        print '     -> Total Thread Count: ',cmo.getHoggingThreadCount()
        print '     -> Idle Thread Count: ',cmo.getExecuteThreadIdleCount()
        print '     -> Queue Length: ',cmo.getQueueLength()
        print '     -> Hogging Thread Count: ',cmo.getHoggingThreadCount()
        print '     -> Throughput: ',cmo.getThroughput()
        print '  -> Threads Details(not idle state) '
        for t in cmo.getExecuteThreads():
          if t.isIdle() == 0 :
            print '     ->  Thread Name: ', t.getName()
            print '     ->  Module Name: ', t.getModuleName()
            print '     ->  User Name: ', t.getUser()
            print '     ->  Work Manager Name: ', t.getWorkManagerName()
            print '     ->  Stuck: ', t.isStuck()
            print '     ->  Hogger: ', t.isHogger()
            print '     ->  Standby: ', t.isStandby()
            print '     ->  Current Request: ', t.getCurrentRequest()
            print
      except WLSTException,e:
        print 'Error description: ', e

def monitorSockets():
    openSession()
    print
    print '**************************************************************'
    print '************* Domain: ',getDomainName()
    print '************* Monitor Sockets ********************************'
    print '************* Collect Date: ',strftime("%a, %d %b %Y %H:%M:%S", localtime())

    print '************* Monitor Sockets ********************************'
    print '************* Collect Date: ',strftime("%a, %d %b %Y %H:%M:%S", localtime())
    print '**************************************************************'
    serverNames = getRunningServerNames()
    domainRuntime()
    for name in serverNames:
        try:
            cd('/ServerRuntimes/'+name.getName())
            print '  -> Server Name: ', name.getName()
            print '     -> Open Sockets: ', cmo.getSocketsOpenedTotalCount()
        except WLSTException,e:
            print 'Error description: ', e
    print ''

def getThreadDumps():
    openSession()
    print
    print '**************************************************************'
    print '************* Domain: ',getDomainName()
    print '************* Thread dumps ********************************'
    print '************* Collect Date: ',strftime("%a, %d %b %Y %H:%M:%S", localtime())
    print '**************************************************************'
    serverNames = getRunningServerNames()
    domainRuntime()
    for name in serverNames:
        try:
            cd('/ServerRuntimes/'+name.getName())
            print '  -> Server Name: ', name.getName()
            print threadDump(writeToFile='false',serverName=name.getName())
        except WLSTException,e:
            print 'Error description: ', e
    print ''

if __name__== "main":

   redirect('/dev/null','false')
   argc = len(sys.argv)
   if argc != 4 :
     usage()
     sys.exit(0)
   uconfigfile=sys.argv[1]
   ukeyfile=sys.argv[2]
   url=sys.argv[3]
   monitorThreads()
   monitorSockets()
   getThreadDumps()
   import time
   time.sleep(10)
   monitorThreads()
   monitorSockets()
   getThreadDumps()
