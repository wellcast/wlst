from WeblogicDomain import WeblogicDomain
import sys
import getopt
import time

if __name__ == "main":

	domainName = 'COH_AR_HMG_DOM01'
	home_path = '/u08/oracle'

	wlsDomain = WeblogicDomain(domainName, home_path)
	