#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import paramiko
import sys
import Client
import time
import getopt

usage = """
Usage:
\tpython3 run.py -b port_begin -e port_end -i ip_address
Example:
\ttpython3 run.py -b1024 -e65535 -i19.18.8.9"""

opts, args = getopt.getopt(sys.argv[1:], 's:c:p:b:e:i:z:h', ["server_timeout=", "client_time_out=",
                                                          "ssh_port=", "begin_port=", "end_port=",
                                                          "ip_address=", "chunk_size=", "help"])


port_begin: int = 1024
port_end: int = 65535
port: int = 22
FL: list = []
chunk: int = 500
srv_timeout: int = 5
host: str = '127.0.0.1'
user = 'root'
password = ''

for o, a in opts:
    if o in ('-b', '--port_begin'): port_begin = int(a)
    if o in ('-e', '--port_end'): port_end = int(a)
    if o in ('-p', '--ssh_port'): port = int(a)
    if o in ('-z', '--chunk_size'): chunk = int(a)
    if o in ('-s', '--server_timeout'): srv_timeout = int(a)
    if o in ('-i', '--ip_address'): host = a
    if o in ('-u', '--user'): user = a
    if o in ('-w', '--password'): password = a
    if o in ('-h', '--help'):
        print(usage)
        sys.exit(0)

ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_client.connect(hostname=host, port=port, username=user, password=password,  look_for_keys=True, allow_agent=True)

ftp_client = ssh_client.open_sftp()
ftp_client.put('Server.py', '/tmp/Server.py')
ftp_client.close()

full = (port_end - port_begin) // chunk
tale = (port_end - port_begin) % chunk

print("full {} tale {} {} {}".format(full, tale, port_end, port_begin) )

for i in range(0, full):
    chunk_begin = port_begin+(chunk*i)
    chunk_end = port_begin+(chunk*i)+chunk
    print("Port range",chunk_begin , chunk_end-1)
    stdin, stdout, stderr = ssh_client.exec_command(
        "python3 /tmp/Server.py {0} {1} {2} &".format(chunk_begin, chunk_end, srv_timeout))
    time.sleep(3);
    FL = Client.scanRange(chunk_begin, chunk_end)

if tale > 0:
    chunk_begin = chunk_end if full > 0 else  port_begin
    chunk_end = chunk_end + tale if full > 0 else  port_end
    print("Port range",chunk_begin , chunk_end, tale )
    stdin, stdout, stderr = ssh_client.exec_command(
        "python3 /tmp/Server.py {0} {1} {2} &".format(chunk_begin, chunk_end, srv_timeout))
    time.sleep(3);
    FL = Client.scanRange(chunk_begin, chunk_end, host)


F = open("openports.txt", "a")
FL = sorted(FL)
F.writelines(list("%s\n" % item for item in FL))
F.close()
ssh_client.close()