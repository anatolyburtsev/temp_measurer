#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 29/10/2014 Anatoly Burtsev onotole@yandex-team.ru
#TODO read GRAPHITE_HOST and PORT from config

import os
import os.path
import sys
import socket
import subprocess as sb
import time

GRAPHITE_HOST = "localhost"
GRAPHITE_PORT = 2003
HOST = socket.gethostname().split('.')[0]
TDIR='/sys/devices/platform/'

#activate coretemp module of kernel
command = "modprobe coretemp".split()
P = sb.Popen( command, stdout=sb.PIPE, stderr=sb.PIPE )
out, err = P.communicate()
sys.stderr.write(err)


tree = os.walk(TDIR)
max_temp = 0

for d, dirs, files in tree:
    for f in files:
        if 'input' in f:
            tfile = open( os.path.join(d,f), 'r')
            max_temp = max( max_temp, tfile.read() )
            tfile.close()

max_temp = int(max_temp) / 1000

#send to graphite
MESSAGE = 'stats.tempmeasurer.%s.cpu %d %d\n' % (HOST, max_temp, int(time.time()))
#print(MESSAGE)
sock = socket.create_connection( (GRAPHITE_HOST, GRAPHITE_PORT))
sock.sendall( MESSAGE )
sock.close()
