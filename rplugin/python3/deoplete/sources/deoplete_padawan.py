#=============================================================================
# FILE: deoplete_padawan.py
# AUTHOR: Pawel Bogut
# Based on:
#   https://github.com/mkusher/padawan.vim
#   https://github.com/zchee/deoplete-jedi
#=============================================================================

from .base import Base
from os import path
from urllib.error import URLError
import sys
import re

sys.path.insert(1, path.dirname(__file__) + '/deoplete_padawan')

import padawan_server


class Source(Base):

    def __init__(self, vim):
        Base.__init__(self, vim)

        self.name = 'padawan'
        self.mark = '[padawan]'
        self.filetypes = ['php']
        self.rank = 500
        self.input_pattern = r'\w+|[^. \t]->\w*|\w+::\w*|\w\(\w*|\\\w*|\$\w*'
        self.current = vim.current
        self.vim = vim

    def on_init(self, context):
        server_addr = self.vim.eval('deoplete#sources#padawan#server_addr')
        server_command = self.vim.eval('deoplete#sources#padawan#server_command')
        log_file = self.vim.eval('deoplete#sources#padawan#log_file')

        self.server = padawan_server.Server(server_addr, server_command,
                                            log_file)

    def get_complete_position(self, context):
        pattern = r'[\'"]\w*|\w*$'
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
            if self.vim.eval('deoplete#sources#padawan#server_autostart') == 1:
                self.server.start()
                self.vim.command("echo 'Padawan.php server started automatically'")
            else:
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
