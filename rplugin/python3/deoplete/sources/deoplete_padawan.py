#=============================================================================
# FILE: deoplete_padawan.py
# AUTHOR: Pawel Bogut
# Based on:
#   https://github.com/mkusher/padawan.vim
#   https://github.com/zchee/deoplete-jedi
#=============================================================================

from .base import Base
from os import path
from urllib.parse import urlencode, urlparse, quote_plus
from urllib.request import urlopen
from urllib.error import URLError
import re
import json
import subprocess


class Server:

    def __init__(self, server_addr, server_command='padawan-server',
                 padawan_path='/tmp'):
        self.server_addr = server_addr
        self.server_command = server_command
        self.padawan_path = padawan_path

    def start(self):
        command = '{0} > {1}/logs/padawan-server.log'.format(
            self.server_command,
            self.padawan_path
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
            1000
        )
        data = json.loads(response.read().decode('utf8'))

        return data


class Source(Base):

    def __init__(self, vim):
        Base.__init__(self, vim)

        self.name = 'padawan'
        self.mark = '[padawan]'
        self.filetypes = ['php']
        self.rank = 500
        self.input_pattern = r'\w+|[^. \t]->\w*|\w+::\w*|\w\(\w*|\\\w*|\$\w*'
        self.current = vim.current

    def on_init(self, context):
        vars = context['vars']
        server_addr = vars.get('deoplete#sources#padawan#server_addr',
                               'http://127.0.0.1:15155')
        server_command = vars.get('deoplete#sources#padawan#server_command',
                                  'padawan-server')
        padawan_path = vars.get('deoplete#sources#padawan#padawan_path',
                                '/tmp')
        self.server = Server(server_addr, server_command, padawan_path)

    def get_complete_position(self, context):
        pattern = r'\w*$'
        m = re.search(pattern, context['input'])
        return m.start() if m else -1

    def gather_candidates(self, context):
        file_path = self.current.buffer.name
        current_path = self.get_project_root(file_path)

        [line_num, _] = self.current.window.cursor
        column_num = context['complete_position'] + 1
        contents = "\n".join(self.current.buffer)

        params = {
            'filepath': file_path.replace(current_path, ""),
            'line': line_num,
            'column': column_num,
            'path': current_path
        }
        result = self.do_request('complete', params, contents)

        candidates = []

        if not result or not 'completion' in result:
            return candidates

        for item in result['completion']:
            candidate = {'word': item['name'],
                         'abbr': item['name'],
                         'kind': item['signature'],
                         'info': item['description'],
                         'dup': 1}
            candidates.append(candidate)

        return candidates

    def do_request(self, command, params, data=''):
        try:
            return self.server.sendRequest(command, params, data)
        except URLError:
            self.vim.command("echo 'Padawan.php is not running'")
        # any other error can bouble to deoplete
        return False

    def get_project_root(self, file_path):
        current_path = path.dirname(file_path)
        while current_path != '/' and not path.exists(
                path.join(current_path, 'composer.json')
        ):
            current_path = path.dirname(current_path)

        if current_path == '/':
            current_path = path.dirname(file_path)

        return current_path
