# Better to use Secure Config File approach for login as shown here http://buttso.blogspot.com/2011/02/using-secure-config-files-with-weblogic.html
connect('weblogic','welcome1','t3://localhost:7001')






# Navigate to the Server Runtime and get the Server Name

serverRuntime()

serverName = cmo.getName()






# Multiple JMS Servers could be hosted by a single WLS server

cd('JMSRuntime/' + serverName + '.jms' )

jmsServers=cmo.getJMSServers()






# Find the list of all JMSServers for this server

namesOfJMSServers = ''
for jmsServer in jmsServers:

namesOfJMSServers = jmsServer.getName() + ' '





# Count the number of connections

jmsConnections=cmo.getConnections()

print str(len(jmsConnections)) + ' JMS Connections found for ' + serverName + ' with JMSServers ' + namesOfJMSServers






# Recurse the MBean tree for each connection and pull out some information about consumers

for jmsConnection in jmsConnections:

try:


  print 'JMS Connection:'
  print '  Host Address = ' + jmsConnection.getHostAddress()

  print '  ClientID = ' + str( jmsConnection.getClientID() )

  print '  Sessions Current = ' + str( jmsConnection.getSessionsCurrentCount() )

  jmsSessions = jmsConnection.getSessions()

  for jmsSession in jmsSessions:

  jmsConsumers = jmsSession.getConsumers()

  for jmsConsumer in jmsConsumers:

    print '  Consumer:'
    print '    Name = ' + jmsConsumer.getName()

    print '    Messages Received = ' + str(jmsConsumer.getMessagesReceivedCount())

    print '    Member Destination Name = ' + jmsConsumer.getMemberDestinationName()

except:

  print 'Error retrieving JMS Consumer Information'
  dumpStack()






# Cleanup

disconnect()

exit()
