#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import sys
import threading

def createServerSocket(port, timeout):
    sock = socket.socket()
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        sock.bind(('', port))
        sock.listen(1)
        sock.settimeout(timeout)
        conn, addr = sock.accept()
        #print('connected:', addr)
        conn.settimeout(timeout)
        data = conn.recv(1024)
        conn.send(data.upper())
        #print(data)
        conn.close()
    except Exception as e:
        print("Error port {0}:  {1}\n".format(port, e))
    finally:
        sock.close()

if len(sys.argv)<2:
    sys.exit(1)

port_begin = int(sys.argv[1])
port_end = int(sys.argv[2])+1

threads = list()

print(len(sys.argv))
if len(sys.argv) == 4:
    timeout = int(sys.argv[3])
else:
    timeout = 3

for i in range(port_begin, port_end):
    x = threading.Thread(target=createServerSocket, args=(i, timeout,))
    threads.append(x)
    x.start()

for i in threads:
    i.join()



