#!/usr/bin/python
# -*- coding: utf-8 -*-
# $Revision: 79 $
# $Date: 2012-08-30 16:53:51 +0200 (Do, 30. Aug 2012) $

import os
import paramiko

class ConnectionSSH(object):
    def __init__(self, host, username = None, password = None, port = None):
        if not port:
            port = 22
        self._trans = paramiko.Transport((host, port))
        self._trans.connect(username = username, password = password)
           
    def execute(self, command):
        channel = self._trans.open_session()
        channel.exec_command(command)
        output = channel.makefile('rb', -1).readlines()
        if output:
            return output  
        
    def close(self):
        #self._sftp.close()
        self._trans.close()
    
    def __del__(self):
        self.close()