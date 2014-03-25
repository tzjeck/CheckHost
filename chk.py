# Author: Adnan Bekan
# 2014  GNU GPL v3


# install Python Package Index
# ---->  sudo apt-get install python-pip	 	
# install xivel library that is published to PyPI
# ---->  sudo pip install xively-python
# install ipaddr module that is published to PyPI
# ---->  sudo pip install ipaddr

import sys
import xively
try:
	import datetime
	import subprocess
	import fileinput
	import socket
	import multiprocessing
	import getopt
	import ipaddr
	
except ImportError, e:
	print 'Error while importing:', str(e)
	sys.exit(1)

#data from your XIVELY account
XIVELY_API_KEY=""
XIVELY_FEED_ID=""

def update(id,val):
	api = xively.XivelyAPIClient(XIVELY_API_KEY)
	feed = api.feeds.get(XIVELY_FEED_ID)
	now = datetime.datetime.now()
	feed.datastreams = [ xively.Datastream(id=id, current_value=val)]
	feed.at=now;
	try:
		feed.update();
	except (requests.HTTPError,  requests.ConnectError) as e:
		print "Error({0}): {1}".format(e.errno, e.strerror)	

def ping_ipv6(id,ip):

	try:
		RESPONSE = subprocess.call('ping6 -c 1 %s' % ip, shell=True, stdout = open('/dev/null', 'w'), stderr=subprocess.STDOUT)
	except:
		print "Error"
	if RESPONSE == 0:
		print 'Node is Alive %s' % ip
	elif RESPONSE == 2: 
		print 'No response %s' % ip
	else:
		print 'Not Alive %s' % ip
	if id != '-1':	
		update(id,RESPONSE) 

def ping_ipv4(id,ip):

	try:
		RESPONSE = subprocess.call('ping -c 1 %s' % ip, shell=True, stdout = open('/dev/null', 'w'), stderr=subprocess.STDOUT)
	except:
		print "Error"
	if RESPONSE == 0:
		print 'Node is Alive %s' % ip
	elif RESPONSE == 2: 
		print 'No response %s' % ip
	else:
		print 'Not Alive %s' % ip
	if id != '-1':	
		update(id,RESPONSE) 
		
def ping(data):
	id,ip=data.split(';')
	ip = ip.lstrip()
	ip = ip.rstrip()
	ip.strip()
	addr=ipaddr.IPAddress(ip)
	if addr.version == 4:
		ping_ipv4(id,ip)
	elif addr.version == 6:
		ping_ipv6(id,ip)
	else:
		print 'Error - not valid IPv4 nor IPv6 address'
	
def help():
	print sys.argv[0] + ': missing argument'
	print 'Try \'' + sys.argv[0] + ' --help\' for more options.'
	
def main():
	try:
		opts, args = getopt.getopt(sys.argv[1:], "hi:f:", ["help", "ip-address=", "filename="])
	except getopt.GetoptError, e:
		print "GetoptError:", str(e)
		help()
		sys.exit(1)
	for o, a in opts:
		if o in ("-h", "--help"):
			print 'Usage: ' + sys.argv[0] + ' [ -f filename] [ -i ip-address] '
			print 'File format -> id;ip'
			sys.exit()
		elif o in ("-i", "--ip-address"):
			IPADDRESS = a
			try:
				ping('-1;'+IPADDRESS)
			except:
				print 'Unspecified Error'
		elif o in ("-f", "--filename"):
			FILENAME = a
			LIST = fileinput.input(FILENAME)
			if __name__ == '__main__':
				PSIZE = multiprocessing.cpu_count() * 4
				P = multiprocessing.Pool(processes=PSIZE)
				P.map(ping, LIST)
				P.close()
				P.join()
		else:
			print "Unhandled Option"

if __name__ == "__main__":
	main()
