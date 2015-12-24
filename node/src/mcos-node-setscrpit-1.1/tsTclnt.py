from socket import *
import sys

if len(sys.argv) < 3:
    print "ths number of argv is few"
    sys.exit(1)

HOST = sys.argv[1]
data = sys.argv[2]
PORT = 21567
BUFSIZ = 1024
ADDR = (HOST, PORT)

tcpCliSock = socket(AF_INET, SOCK_STREAM)
tcpCliSock.connect(ADDR)
tcpCliSock.send(data)
data1 = tcpCliSock.recv(BUFSIZ)
print data1
tcpCliSock.close()
