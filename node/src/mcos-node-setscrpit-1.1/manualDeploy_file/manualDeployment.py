#!/usr/bin/python
import sys
import os
import string
import string
import ConfigParser
from socket import *
from time import sleep
from time import ctime
import threading
import logging
import logging.handlers
import sys
reload(sys)
sys.setdefaultencoding('utf8')

handler = logging.handlers.RotatingFileHandler('/var/log/openstackDeploy.log',maxBytes = 1024*1024, backupCount = 5)
fmt = '%(asctime)s-%(filename)s:%(lineno)s-%(name)s-%(message)s'
formatter = logging.Formatter(fmt)
handler.setFormatter(formatter)
logger = logging.getLogger('*****')
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

conf = ConfigParser.ConfigParser()
conf.read("/etc/openstack_deploy.conf")
if not conf.has_section("deployinfo"):
	conf.add_section("deployinfo")
	conf.set("deployinfo","deploystatus","nodeploy")
lastDeployStatus = conf.get("deployinfo","deploystatus")
conf.set("deployinfo","deploystatus","deploying")
conf.write(open("/etc/openstack_deploy.conf","w"))

list = []
if os.path.exists("/etc/nodeHardwareInfo/nodesum.conf"):
	confNodeSum = ConfigParser.ConfigParser()
	confNodeSum.read("/etc/nodeHardwareInfo/nodesum.conf")
	if confNodeSum.has_section("newaddnodes"):
		nodesum = confNodeSum.get("newaddnodes","newnodesum").strip('\n')
		for i in range(string.atoi(nodesum)):
			newNodeName = confNodeSum.get("newaddnodes","node"+str(i+1)).strip('\n')
			list.append(newNodeName)

globalStr = ""
BUFSIZ = 1024

def getServiceStatus(ip, cmd):
	ret = -1
	ssh = pexpect.spawn('ssh root@%s "%s"' % (ip, cmd))
	try:
		i = ssh.expect(['password:', 'continue connecting (yes/no)?'], timeout=5)
		if i == 0 :
			ssh.sendline(conf.get("nodeloginfo","nodepasswd").strip('\n'))
			ssh.sendline(cmd)
			rInfo=ssh.read()
			if "Active: active (running)" in rInfo:
				ret = 0
			else:
				ret = -1
		elif i == 1:
			ssh.sendline('yes\n')
			ssh.expect('password: ')
			ssh.sendline(conf.get("nodeloginfo","nodepasswd").strip('\n'))
			ssh.sendline(cmd)
			r = ssh.read()
			if "Active: active (running)" in r:
				ret = 0
			else:
				ret = -1
	except pexpect.EOF:
		print "EOF"
		ssh.close()
		ret = -1
	except pexpect.TIMEOUT:
		print "TIMEOUT"
		ssh.close()
		ret = -2
	return ret

class MyThread(threading.Thread):
	#print("come in mythread")
	def __init__(self,threadName,event):
		threading.Thread.__init__(self,name=threadName)

		self.threadEvent = event
		HOST = conf.get("nodeip","hostip").strip('\n')
		PORT = 21567
		BUFSIZ = 1024
		ADDR = (HOST, PORT)
		s1 = self.tcpSerSock = socket(AF_INET, SOCK_STREAM)
		s2 = self.tcpSerSock.bind(ADDR)
		s3 = self.tcpSerSock.listen(5)
		print ("s1 = %s , s2 = %s, s3 = %s" %(s1 ,s2, s3))
		logger.info("socket = %s , band = %s, listen = %s" %(s1 ,s2, s3))
	def run(self):
		while True:
			print 'waiting for connection...'
			logger.info('waiting for connection...')
			tcpCliSock, addr = self.tcpSerSock.accept()
			print '...connected from:', addr
			logger.info('...connected from:'+str(addr))
			while True:
				data = tcpCliSock.recv(BUFSIZ)
				if not data:
					print ("data is null!")
					logger.info("return deploy info is null!")
					break
				tcpCliSock.send('[%s] %s' %(ctime(), data))
				print("send info is:%s,%s" %(ctime(),data))
				if("success" in data or "failed" in data):
					global globalStr
					globalStr = data
					print("come in set()")
					self.threadEvent.set()
			tcpCliSock.close()
		tcpSerSock.close()

def getNeutronScriptToController():
	if conf.get("networkinfo","networktype") == 'gre':
		return "network-gre"
	if conf.get("networkinfo","networktype") == 'vlan':
		return "network-vlan"
	if conf.get("networkinfo","networktype") == 'vxlan':
		return "network-vxlan"

def getNeutronScriptToComputer():
	if conf.get("networkinfo","networktype") == 'gre':
		return "computer-gre"
	if conf.get("networkinfo","networktype") == 'vlan':
		return "computer-vlan"
	if conf.get("networkinfo","networktype") == 'vxlan':
		return "computer-vxlan"

def deployOpenstack():
	signal = threading.Event()
	checkThead = MyThread('checkThread',signal)
	checkThead.start()
	
	for opstkComponentNum in range(string.atoi(conf.get("componentorder","componentnum"))):
		opstkCom = conf.get("componentorder","comorder"+str(opstkComponentNum))
		print("====================================================")
		print("           start deploy %s" %opstkCom)
		print("====================================================")
		logger.info("====================================================")
		logger.info("           start deploy %s" %opstkCom)
		logger.info("====================================================")
		logger.info("deploying ...")
		if not conf.get("deploytype","typevalue") == "computer":
                        if opstkCom == "mysql":
                                command = 'setup-mysql'

                        if opstkCom == "rabbitmq":
                                command = "setup-rabbitmq"

                        if opstkCom == "keystone":
                                command = "setup-controller-keystone"
                        
                        if opstkCom == "nfs":
                                continue
                        if opstkCom == "controller-glance":
                                command = "setup-controller-glance"
                
                        if opstkCom == "controller-nova":
                                if conf.get("deploytype","typevalue") == "allinone":
                                        command = "setup-controller-nova allinone"
                                else:
                                        command = "setup-controller-nova"

                        if opstkCom == "controller-neutron":
                                opstkCom = getNeutronScriptToController()
                                if opstkCom == "network-gre":
                                        command = "setup-network-gre-node"
                                if opstkCom == "network-vlan":
                                        command = "setup-network-vlan-node"
                                if opstkCom == "network-vxlan":
                                        command = "setup-network-vxlan-node"
                                opstkCom = "controller-neutron"
                        if opstkCom == "neutron":
                                continue
                        if opstkCom == "controller-cinder":
                                command = "setup-controller-cinder"

                        if opstkCom == "controller-horizon":
                                command = "setup-controller-horizon"
                                
                        if opstkCom == "controller-heat":
                                continue

                        if opstkCom == "cinder":
                                command = "setup-store-cinder /dev/sda2"

                        if opstkCom == "computer":
                                continue
                                opstkCom = "computer"
                        if opstkCom == "mongodb":
                                command = "setup-mongodb" 
                        if opstkCom == "controller-ceilometer":
                                command = "setup-controller-ceilometer"
                        if opstkCom == "ceilometer-snmp" and conf.get("deploytype","typevalue") == "allinone":
                                command = "setup-ceilometer-snmp"
                else:
			if opstkCom == "computer" or opstkCom == "ceilometer-snmp":
                        	if opstkCom == "computer":
                        	        opstkCom = getNeutronScriptToComputer()
                        	        if opstkCom == "computer-gre":
                        	                command = "setup-compute-gre-node"
                        	        if opstkCom == "computer-vlan":
                        	                command = "setup-compute-vlan-node"
                        	        if opstkCom == "computer-vxlan":
                        	                command = "setup-compute-vxlan-node"
                        	        opstkCom = "computer"
                       		if opstkCom == "ceilometer-snmp":
                                	command = "setup-ceilometer-snmp"
			else:
				continue
		logger.info("##**##&start:"+opstkCom)
		os.system(command)
		#execRemoteCommond(conf.get("nodeip",nodeName+"_ip"),command)
		if not opstkCom == "computer":
			signal.wait()
			signal.clear()
		logger.info("##**##&end:"+globalStr)
		print("##**##&end:"+globalStr)
		if "failed" in globalStr:
			conf.set("deployinfo","deploystatus","deployed")
			conf.write(open("/etc/openstack_deploy.conf","w"))

if __name__ == '__main__':
	deployOpenstack()
	print("##**##&deployover")
	logger.info("##**##&deployover")
	conf.set("deployinfo","deploystatus","deployed")
	conf.write(open("/etc/openstack_deploy.conf","w"))
	print ("****************************************************")
	print ("                openstack deploy over               ") 
	print ("****************************************************")
	logger.info("****************************************************")
	logger.info("                openstack deploy over               ")
	logger.info("****************************************************")
	os._exit(0)
