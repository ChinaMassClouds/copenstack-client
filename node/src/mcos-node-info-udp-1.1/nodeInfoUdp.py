# -*- coding: utf-8 -*-

import socket,traceback

host = ''
port = 6666

import json
import os
import time
import commands
import sys

def kill_udp_process():
    outputValue = commands.getstatusoutput("ps aux | grep nodeInfoUdp.py | grep -v grep | awk '{print $2}'")
    if outputValue[0] == 0:
        #print outputValue
        self_pid = os.getpid()
        for pid in outputValue[1].split("\n"):
            #print pid, self_pid
            if pid != str(self_pid): 
                os.system("kill -9 %s &> /dev/null" % pid)

def has_udp_process():
    outputValue = commands.getstatusoutput("ps aux | grep nodeInfoUdp.py | grep -v grep | awk '{print $2}'")
    if outputValue[0] == 0:
        #print outputValue
        self_pid = os.getpid()
        pid_list = outputValue[1].split("\n")
        if len(pid_list) > 1:
            return True

    return False

def get_client_node_info():
    os.system('facter > /root/facter.txt')
    client_node_info = {}
    with open(r'/root/facter.txt') as facterfile:
        for line in facterfile:
            itemList = line.split(" => ")
            if len(itemList) > 1:
                if itemList[1].startswith("{"):
                    replaceValue = itemList[1][0:-1].replace("=>", ":")
                    jsonValue = json.loads(replaceValue)
                    client_node_info[itemList[0]] = jsonValue
                else:
                    client_node_info[itemList[0]] = itemList[1][0:-1]
        outputValue = commands.getstatusoutput("pvs | grep -v PV | awk '{print $1}'")
        if outputValue[0] == 0:
            client_node_info["pvlist"] = outputValue[1].split("\n")
                
    return  json.dumps(client_node_info)

def start_udp_listen():
    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    s.setsockopt(socket.SOL_SOCKET,socket.SO_BROADCAST,1)
    s.bind((host,port))
    print "Listen on the port 6666......"

    while True:
        try:
            data,addr = s.recvfrom(8192)
            if data == "Request Hardware Information":
                print "Receive data from:",addr, data
                os.system("sed  -i '/master.server.com/d' /etc/hosts")
                os.system("echo -e '%s  master.server.com' >> /etc/hosts" % addr[0])
                os.system("systemctl enable puppet && systemctl start puppet")
                os.system("systemctl status puppet")
                node_info = get_client_node_info()
                s.sendto(node_info, addr)
            elif data == "Puppet client node Authentication":
                #os.system("puppet agent -t")
                print "puppet"
            elif data == "Restart puppet service":
                os.system("systemctl restart puppet")
        except (KeyboardInterrupt,SystemExit):
            raise
        except:
            traceback.print_exc()
 
       
if len(sys.argv) > 1:
    if sys.argv[1] == "stop":
        print "stop the node udp listen service"
        kill_udp_process()
    elif sys.argv[1] == "restart":
        print "restart the node udp listen service"
        kill_udp_process()
        start_udp_listen()
    elif sys.argv[1] == "start":
        print "start the node udp listen service"
        if not has_udp_process():
            start_udp_listen()
    elif sys.argv[1] == "status":
        if has_udp_process():
            print "the sevice is running"
        else:
            print "the service is stop"



