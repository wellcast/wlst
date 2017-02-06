jmsserver='AcmeCommonJmsServer'
jmsmodule='WSMTestJMSModule'
jmsqueue='WSMTestJMSDQ'

for i in range (1,5):
   connect('weblogic', 'weblogic1', 't3://acme-osbpp1ms' + str(i) + '.pippo.com:8001')
   serverRuntime()
   cd('JMSRuntime')
   cd('osbpp1ms' + str(i) + '.jms')
   cd('JMSServers')
   cd(jmsserver + str(i))
   cd('Destinations')
   cd(jmsmodule + '!' + jmsserver + str(i) + '@' + jmsqueue)
   cmo.deleteMessages('')
   disconnect()

----

from javax.naming import Context, InitialContext
from weblogic.jndi import WLInitialContextFactory
from javax.jms import QueueSession, Queue, Session

properties = Properties()
properties[Context.PROVIDER_URL] = "t3://localhost:7001"
properties[Context.INITIAL_CONTEXT_FACTORY] = WLInitialContextFactory.name
ctx = InitialContext(properties)

connectionFactory = ctx.lookup("weblogic/jms/XAConnectionFactory" )
queueCon = connectionFactory.createQueueConnection();
queueSession = queueCon.createQueueSession( false, Session.AUTO_ACKNOWLEDGE );
queue = ctx.lookup( "jms/testme")
sender = queueSession.createSender( queue );

msg = queueSession.createTextMessage( "<hello>I am a pig</hello>" );

sender.send( msg );
