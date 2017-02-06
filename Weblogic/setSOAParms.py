#redirect('/dev/null', 'false')

connect ('weblogic', '', 't3://01:10001')

domainRuntime()

SOAInfraConfigobj = ObjectName('oracle.as.soainfra.config:Location=soa_ms0101,name=bpel,type=BPELConfig,Application=soa-infra')

mbs.getAttribute(SOAInfraConfigobj,'SyncMaxWaitTime')
mbs.setAttribute(SOAInfraConfigobj, Attribute('SyncMaxWaitTime',90))

disconnect()
exit()
