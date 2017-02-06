##
## Script para configuracao basica de dominios Weblogic
##

## 1 - Server Start (classpath, args, java, etc)
## 2 - Logs
## 3 - Datasources

## 
## Como dexecutar
## cd /u01/oracle/soa/middleware/scripts
## /u01/oracle/soa/middleware/fmw12c/wlserver/common/bin/wlst.sh configDomain.py

##### Parâmetros #####
username='weblogic'
password=''
domainURI='t3://10.2.0.58:9001'
logPath='/u01/oracle/soa/logs/SOAHml_Domain/'
AdminSrv='soa-hml-adm'
JavaHome='/u01/oracle/soa/middleware/java/jdk17'
JavaVendor='Oracle'
WlsInstallDir='/u01/oracle/soa/middleware/fmw12c/wlserver_10.3'
DomainDir='/u01/oracle/soa/domains/SOAHml_Domain'

# ClassPath em funcao do produto
# Exemplo /u01/oracle/soa/domains/SOAHml_Domain/bin/startManagedWebLogic.sh soa-hml-inst01 http://OFMWHMLSOA01:9001
ClassPath='/u01/oracle/soa/middleware/fmw12c/soa/bam/lib/bam-timerlistener.jar:/u01/oracle/soa/middleware/fmw12c/soa/soa/modules/user-patch.jar:/u01/oracle/soa/middleware/fmw12c/soa/soa/modules/soa-startup.jar:/u01/oracle/soa/middleware/fmw12c/oracle_common/modules/features/com.oracle.db.jdbc7-dms.jar:/u01/oracle/soa/middleware/java/jdk17/lib/tools.jar:/u01/oracle/soa/middleware/fmw12c/wlserver/server/lib/weblogic_sp.jar:/u01/oracle/soa/middleware/fmw12c/wlserver/server/lib/weblogic.jar:/u01/oracle/soa/middleware/fmw12c/wlserver/../oracle_common/modules/net.sf.antcontrib_1.1.0.0_1-0b3/lib/ant-contrib.jar:/u01/oracle/soa/middleware/fmw12c/wlserver/modules/features/oracle.wls.common.nodemanager_2.0.0.0.jar:/u01/oracle/soa/middleware/fmw12c/soa/soa/modules/oracle.soa.common.adapters_11.1.1/oracle.soa.common.adapters.jar:/u01/oracle/soa/middleware/fmw12c/soa/soa/modules/oracle.cloud.adapter_12.1.3/oracle.cloud.adapter.jar:/u01/oracle/soa/middleware/fmw12c/osb/lib/servicebus-common.jar:/u01/oracle/soa/middleware/fmw12c/oracle_common/communications/modules/config-12.1.3.jar:/u01/oracle/soa/middleware/fmw12c/oracle_common/communications/modules/userprefs-config-12.1.3.jar:/u01/oracle/soa/middleware/fmw12c/oracle_common/modules/oracle.xdk_12.1.3/xsu12.jar:/u01/oracle/soa/middleware/fmw12c/wlserver/../modules/features/weblogic.server.modules.xquery_10.3.1.0.jar:/u01/oracle/soa/middleware/fmw12c/soa/soa/modules/db2jcc4.jar:/u01/oracle/soa/domains/SOAHml_Domain/config/soa-infra:/u01/oracle/soa/middleware/fmw12c/soa/soa/modules/fabric-url-handler_11.1.1.jar:/u01/oracle/soa/middleware/fmw12c/soa/soa/modules/quartz-all-1.6.5.jar:/u01/oracle/soa/middleware/fmw12c/soa/soa/modules/oracle.soa.fabric_11.1.1/oracle.soa.fabric.jar:/u01/oracle/soa/middleware/fmw12c/soa/soa/modules/oracle.soa.fabric_11.1.1/fabric-runtime-ext-wls.jar:/u01/oracle/soa/middleware/fmw12c/soa/soa/modules/oracle.soa.adapter_11.1.1/oracle.soa.adapter.jar:/u01/oracle/soa/middleware/fmw12c/soa/soa/modules/oracle.soa.b2b_11.1.1/oracle.soa.b2b.jar:/u01/oracle/soa/middleware/fmw12c/oracle_common/modules/internal/features/jrf_wlsFmw_oracle.jrf.wls.classpath_12.1.3.jar:/u01/oracle/soa/middleware/fmw12c/soa/soa/modules/oracle.soa.fabric_11.1.1/tracking-api.jar:/u01/oracle/soa/middleware/fmw12c/soa/soa/modules/commons-cli-1.1.jar:/u01/oracle/soa/middleware/fmw12c/soa/soa/modules/oracle.soa.mgmt_11.1.1/soa-infra-mgmt.jar:/u01/oracle/soa/middleware/fmw12c/wlserver/common/derby/lib/derbyclient.jar:/u01/oracle/soa/middleware/fmw12c/wlserver/common/derby/lib/derby.jar:/u01/oracle/soa/middleware/fmw12c/wlserver/server/lib/xqrl.jar'

# Arguments
arguments='-Xms2048m -Xmx2048m -XX:+UnlockCommercialFeatures -XX:+FlightRecorder'

# + Setup WKA Coherence - Well Known Address
# Adaptacao necessaria para cada host (locahost e port tem que ser ajustados)
argswka=' -Dtangosol.coherence.wka1=soa-hml-inst01-priv -Dtangosol.coherence.wka1.port=19101 -Dtangosol.coherence.wka2=soa-hml-inst02-priv -Dtangosol.coherence.wka2.port=19101 -Dtangosol.coherence.localhost=soa-hml-inst01-priv -Dtangosol.coherence.localport=19101'

# Basic tuning
## XmsXmxXns='-Xms2048m -Xmx2048m -Xns512m -Xgc:throughput

# Other options
##'-XXgcThreads=6 -XX:OptThreads=8 -XX:+UseCallProfiling -XXtlasize:min=16k,preferred=1m,wasteLimit=8k -XX:NewSize=128m -XX:MaxNewSize=128m -XX:SurvivorRatio=8 -XX:+HeapDumpOnOutOfMemoryError

# Large Pages
##-XX:+UseLargePagesForHeap

# Mgmt port
##'-Xmanagement:autodiscovery=true,authenticate=false,ssl=false,interface=hostname,port=12566'

# Verbose Gc
##  -verbose:gc -XX:+PrintGCDetails -XX:+PrintGCTimeStamps -Xloggc:/u01/oracle/soa/logs/gc.log

# JFR
## https://docs.oracle.com/javacomponents/jmc-5-4/jfr-runtime-guide/run.htm#JFRUH176
## -XX:+UnlockCommercialFeatures -XX:+FlightRecorder
## jcmd 5368 JFR.start duration=60s filename=myrecording.jfr

# TD
##  /u01/oracle/soa/middleware/java/jdk17/bin/jcmd 4564 Thread.print > /tmp/td4.txt

# Backup antes de toda alteracao - programar backup; Exemplo:
## /u01/oracle/soa/domains/applications/SOAHml_Domain
## /u01/oracle/soa/domains/SOAHml_Domain/config
## /u01/oracle/soa/domains/SOAHml_Domain/servers/soa-hml-adm/data

##### Inicio do Script #####
connect(username,password,domainURI);
edit();
cd('Servers');
server=cmo.getServers();
startEdit();#Alteracao do server start
for x in server:
if x.getName() != AdminSrv:
  cd('/Servers/'+x.getName()+'/ServerStart/'+x.getName());
  if x.getName().startswith('soa'):
   set('Arguments',arguments+argswka+' -Dweblogic.Stdout='+logPath+x.getName()+'/'+x.getName()+'.out'+' -Dweblogic.Stderr='+logPath+x.getName()+'/'+x.getName()+'.out');
  else:
   set('Arguments',arguments+' -Dweblogic.Stdout='+logPath+x.getName()+'/'+x.getName()+'.out'+' -Dweblogic.Stderr='+logPath+x.getName()+'/'+x.getName()+'.out');
  set('JavaHome',JavaHome);
  set('JavaVendor',JavaVendor);
  set('BeaHome',WlsInstallDir);
  set('RootDirectory',DomainDir);
  set('SecurityPolicyFile',WlsInstallDir+'/server/lib/weblogic.policy');
  set('ClassPath',ClassPath);
  save();
#Alteracao dos logs
for x in server:
cd('/Servers/'+x.getName()+'/WebServer/'+x.getName()+'/WebServerLog/'+x.getName());
set('LogFileFormat','extended');
set('ELFFields','c-ip cs-username date time cs-method cs-uri sc-status sc-bytes time-taken bytes');
set('FileMinSize','50000');
set('FileCount','7');
set('LogFileRotationDir',logPath+x.getName());
set('NumberOfFilesLimited','true');
set('FileName',logPath+x.getName()+'/access_%yyyy%_%MM%_%dd%_%hh%_%mm%.log');
set('RotateLogOnStartup','true');
cd('/Servers/'+x.getName()+'/Log/'+x.getName());
set('FileMinSize','50000');
set('FileName',logPath+x.getName()+'/'+x.getName()+'_%yyyy%_%MM%_%dd%_%hh%_%mm%.log');
set('RotateLogOnStartup','true');
set('FileCount','7');
set('LogFileRotationDir',logPath+x.getName());
set('NumberOfFilesLimited','true');
set('RedirectStderrToServerLogEnabled','true');
set('RedirectStdoutToServerLogEnabled','true');
set('ServerLoggingBridgeUseParentLoggersEnabled','true');
save();
#activate();
disconnect();
exit();
