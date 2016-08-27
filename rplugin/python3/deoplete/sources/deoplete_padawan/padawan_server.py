#=============================================================================
# FILE: deoplete_padawan.py
# AUTHOR: Pawel Bogut
#   https://github.com/mkusher/padawan.vim
#=============================================================================
from os import path
from urllib.parse import urlencode, quote_plus
from urllib.request import urlopen
import json
import subprocess


class Server:

    def __init__(self, server_addr, server_command='padawan-server',
                 log_file='/tmp/padawan-server.log'):
        self.server_addr = server_addr
        self.server_command = server_command
        self.log_file = log_file

    def start(self):
        if path.exists(path.dirname(self.log_file)):
            command_str = '{0} > {1}'
        else:
            command_str = '{0}'

        command = command_str.format(
            self.server_command,
            self.log_file
        )
        subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
        )

    def stop(self):
        try:
            self.sendRequest('kill', {})
            return True
        except Exception:
            return False

    def restart(self):
        if self.stop():
            self.start()

    def sendRequest(self, command, params, data=''):
        addr = self.server_addr + "/" + command + "?" + urlencode(params)
        response = urlopen(
            addr,
            quote_plus(data).encode('utf8'),
            3  # can be high as its async call after all
        )
        data = json.loads(response.read().decode('utf8'))

        return data
