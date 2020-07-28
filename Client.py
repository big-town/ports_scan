#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import sys
import threading

FL = []

def createClientSocket(port, timeout, host='127.0.0.1'):
    sock = socket.socket()
    try:
        sock.settimeout(timeout)
        sock.connect((host, port))
        sock.send(bytes(str(port)+"-ok",'utf-8'))
        data = sock.recv(1024)

        if data.decode('utf-8') == (str(port)+"-OK"):
            FL.append(int(port))
            print("Port {} is open!\n".format(port))
        sock.close()
    except Exception as e:
        print("Error port {0}:  {1}\n".format(port, e))
        return None
    finally:
        sock.close()

def scanRange(port_begin, port_end, host):
    threads = list()

    for i in range(port_begin, port_end):
        x = threading.Thread(target=createClientSocket, args=(i, 5, host,))
        threads.append(x)
        x.start()

    for i in threads:
        i.join()
    return FL









