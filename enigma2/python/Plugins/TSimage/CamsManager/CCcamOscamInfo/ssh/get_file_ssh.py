#!/usr/bin/python
# -*- coding: utf-8 -*-
# $Revision: 81 $
# $Date: 2012-08-30 22:56:41 +0200 (Do, 30. Aug 2012) $

from connection_ssh import ConnectionSSH
import re

def ssh_list_tmp(host, port, password, username):
    tmp = []
    ssh_dir_tmp = []
    try:
        s = ConnectionSSH(host = host, port = int(port), username = username, password = password)
        tmp = s.execute('ls /tmp')
        s.close()
        for x in tmp:
            x = x.replace("\n","")
            if x.startswith('ecm'):
                ssh_dir_tmp.append(x)
    except:
        pass
    return ssh_dir_tmp
    
def ssh_grab_ecminfo(host, port, password, username, file):
    tmp = []
    ssh_dir_grab = []
    if 1 == 1:
    #try:
        s = ConnectionSSH(host = host, port = int(port), username = username, password = password)
        tmp = s.execute("tail /tmp/%s" % file)
        s.close()
        ssh_dir_grab = tmp
    #except:
    #    pass
    return ssh_dir_grab
