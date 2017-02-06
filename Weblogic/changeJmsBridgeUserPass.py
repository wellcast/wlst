connect('weblogic','senha','t3://10.0.10.27:22000')
ADMDIR=cmo.getRootDirectory()

edit()
startEdit()

bridges=cmo.getJMSBridgeDestinations()
for b in bridges:
     b.setUserName('jmsbridge')
     b.setUserPasswordEncrypted(encrypt('novasenha', ADMDIR))
     save()

activate(block="true")
disconnect()
