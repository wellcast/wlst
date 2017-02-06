'''
WLST Script to configure Weblogic managed servers with coherence arguments for ATG SQL Repository cache

'''

import time
from time import gmtime, strftime, localtime
#from java.util.regex import *
#from weblogic.management.runtime import ExecuteThread
import sys
import getopt


'''
Init definition

'''
scriptdir="/u08/oracle/scripts"
domainconfigfile="_configfile.secure"
domainkeyfile="_keyfile.secure"
defwluser='atgdeploy'
defwlpass='welcome1'
url="t3://172.16.66.205:7001"
logfile=scriptdir+"/logs/"+strftime("%d%b%Y%H%M%S", localtime())+".log"
#logfileweb=scriptdir+"/logs/"+strftime("%d%b%Y%H%M%S", localtime())+".log"
oracle_home="/u08/oracle"
wlslogspath="/u08/oracle/logs"
wlslogssize='50000'
wlslogslevel='Warning'
xms='2048m'
xmx='2048m'
connected='no'

def usage():
    print "Usage:"
    print "domain_collect.wlst [config_file.secure] [key_file.secure] [t3://admin_url] [server_argumets_file]"

'''
Read and load cfg files

'''
def readCfgFile(flpath):
    f = open(flpath)
    lines = f.read().splitlines()
    cfgarray = {}
    for l in lines:
        #cfgarray[l.split()[0]] = l.split()[1]
        al = l.split(';')
        cfgarray[al[0]] = al[1]
    return cfgarray

'''
Basic operations

'''
def openSession(connected):
    global defwluser, defwlpass, url
    if connected != 'yes':
       try:
         #if domainconfigfile != '':
        #       connect(userConfigFile=domainconfigfile, userKeyFile=domainkeyfile, url=url)
        # else:
        connect(defwluser, defwlpass, url)
        connected='yes'
       except WLSTException,e:
         print 'Error description: ', e
         sys.exit(0)

def editMode():
    edit()
    startEdit()

def editActivate():
    save()
    activate(block="true")

def getDomainName():
    openSession(connected)
    domainConfig()
    cd ('/')
    return cmo.getName()

def getManagedServers():
    openSession(connected)
    serverConfig()
    return cmo.getServers()

def getDatasources():
    openSession(connected)
    serverConfig()
    return cmo.getJDBCSystemResources()

def getAdminServerName():
    openSession(connected)
    domainConfig()
    return cmo.getAdminServerName()


'''
Log files

'''
def getFullAccessPath(baselogpath, domainName, ms):
        return baselogpath+'/'+domainName+'/'+ms+'/access-ms_%yyyy%_%MM%_%dd%_%hh%_%mm%.log'

def getFullLogPath(baselogpath, domainName, ms):
        return baselogpath+'/'+domainName+'/'+ms+'/'+ms+'_%yyyy%_%MM%_%dd%_%hh%_%mm%.log'

def getFullRotatePath(baselogpath, domainName, ms):
        return baselogpath+'/'+domainName+'/'+ms

def getFullOutPath(baselogpath, domainName, ms):
        return baselogpath+'/'+domainName+'/'+ms+'/'+ms+'.log'


'''
Prepare Wls Args based on a model
'''
def replaceArgsVariable(args, domainname, managedname):
    global wlslogspath

    args=args.replace('_XMS',xms)
    args=args.replace('_XMX',xms)
    args=args.replace('_LOG_OUT',getFullOutPath(wlslogspath,domainname,managedname))
    args=args.replace('_LOG_ERR',getFullOutPath(wlslogspath,domainname,managedname))
    args=args.replace('_DOMAIN_PATH',oracle_home+'/domains/'+domainname)

    return args


'''
Confgure managed servers

'''
def setMSsManaged(wlsargs):
    global wlslogspath
    global wlslogssize
    global wlslogslevel

    print "Starting weblogic server start configuration..."
    openSession(connected)

    #sstartargs=readCfgFile(wlsargs)
    domainName=getDomainName()
    adminsrvname=getAdminServerName()
    servers=getManagedServers()

    editMode()

    for s in servers:
        if s.getName() != adminsrvname:
          if s.getName().startswith('atg-ar-prd-nsps'):
            #cd('/Servers/'+s.getName()+'/ServerStart/'+s.getName())
            #print "Managed Server: "+s.getName()
            #print "Current Args: "+s.get('Arguments')
            #farg=replaceArgsVariable(sstartargs[s.getName()], domainName, s.getName())
            #print "New Args: "+farg
            #set('Arguments',farg)

            cd('/Servers/'+s.getName()+'/Log/'+s.getName())
            #set('FileName',getFullLogPath(wlslogspath, domainName, s.getName()))
            set('FileMinSize',wlslogssize)
            #set('LogFileRotationDir',getFullRotatePath(wlslogspath, domainName, s.getName()))
            set('LogFileSeverity',wlslogslevel)
            set('LoggerSeverity',wlslogslevel)
            set('MemoryBufferSeverity',wlslogslevel)
            set('StdoutSeverity',wlslogslevel)

            cd('/Servers/'+s.getName()+'/WebServer/'+s.getName()+'/WebServerLog/'+s.getName())
            set('LogFileFormat','extended')
            set('ELFFields','c-ip cs-username date time cs-method cs-uri sc-status sc-bytes time-taken bytes')
            #set('FileName',getFullAccessPath(wlslogspath, domainName, s.getName()))
            set('LoggingEnabled',False)

            '''
            '''
            cd('/Servers/'+s.getName()+'/ServerDiagnosticConfig/'+s.getName())
            set('WLDFDiagnosticVolume','Off')

            save()


'''
Domain context changes
'''
def setMSsDomain():
    domainname=getDomainName()
    print "Starting weblogic server start configuration..."
    openSession(connected)
    editMode()
    #domainConfig()
    cd('/JTA/'+domainname)
    set('TimeoutSeconds',1200)
    set('AbandonTimeoutSeconds',2400)
    save()

'''
Datasource
'''
def setMSsDatasources():
    print "Starting weblogic server start configuration..."
    openSession(connected)
    datasources=getDatasources()
    editMode()
    for s in datasources:
            cd('/JDBCSystemResources/'+s.getName()+'/JDBCResource/'+s.getName()+'/JDBCConnectionPoolParams/'+s.getName())
            print "DataSource: "+s.getName()
            set('TestTableName','SQL BEGIN NULL; END;')
            set('TestConnectionsOnReserve','true')
            save()


if __name__== "main":
   print "##"
   print "## Log file: "+logfile
   print "##"
   #redirect(logfile,'true')
   #sys.stdout = open(logfile,"w")
   #argc = len(sys.argv)
   #if argc != 5 :
     #usage()
     #sys.exit(0)
   #  domainconfigfile=sys.argv[1]
   #  domainkeyfile=sys.argv[2]
   #  url=sys.argv[3]
   #  serverstartcfg=sys.argv[4]
   #else:
   #serverstartcfg=sys.argv[0]
   #Config sequence
   setMSsManaged('')
   setMSsDatasources()
   #setMSsDomain()

   #activate()

