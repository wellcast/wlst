class WeblogicDomain(object):
	'Weblogic domain definition to setup new environment'

	name = 'sampleDomain'
	default_home = '/u01/oracle/'
	domains_home = 'domains'
	java_home = 'jdk/jdk18'
	adminHttpUrl = 'http://127.0.0.1:7001'
	adminT3Url = 't3://127.0.0.1:7001'
	version = '12.1.3'
	default_user = 'weblogic'
	default_password = '---'
	connected = 'no'


	def __init__(self, name, default_home):
		self.name = name
		self.default_home = default_home

	def connect():
		if connected == 'no':
			try:
				connect(self.default_user,self.default_password,self.adminT3Url)
				self.connected = 'yes'
			except WLSTException, e:
				print 'Error: ', e
				raise e

	def disconnect():
		if connected == 'yes':
			try: 
				disconnect();
				self.connected = 'no'
			except WLSTException, e:
				print 'Error: ', e
				raise e
