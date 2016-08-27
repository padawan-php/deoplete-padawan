# deoplete-padawan

[deoplete.nvim](https://github.com/Shougo/deoplete.nvim) source for
[padawan.php](https://github.com/mkusher/padawan.php).

Deoplete-padawan offers asynchronous completion of code written in PHP using
[padawan.php](https://github.com/mkusher/padawan.php) and
[deoplete.nvim](https://github.com/Shougo/deoplete.nvim).

It requires [neovim](https://github.com/neovim/neovim) as deoplete requires it.

## Installation

You need to install [padawan.php](https://github.com/mkusher/padawan.php) and
index your project. The plugin requires padawan.php server running to work.
Go to project GitHub page for details.

Using [vim-plug](https://github.com/junegunn/vim-plug):
```vim
Plug 'Shougo/deoplete.nvim'

Plug 'pbogut/deoplete-padawan'
```

Using [Vundle](https://github.com/VundleVim/Vundle.vim):
```vim
Plugin 'Shougo/deoplete.nvim'

Plugin 'pbogut/deoplete-padawan'
```

## Configuration

The plugin requires no configuration. However, it is possible to change some
options.

### Available settings

| Variable                                    | Default                 |
|:--------------------------------------------|:------------------------|
| g:deoplete#sources#padawan#server_addr      | http://127.0.0.1:15155  |
| g:deoplete#sources#padawan#server_command   | padawan-server          |
| g:deoplete#sources#padawan#log_file         | /tmp/padawan-server.log |
| g:deoplete#sources#padawan#server_autostart | 1                       |

- `g:deoplete#sources#padawan#server_addr`

Address to padawan.php server. By default, it is `http://127.0.0.1:15155`

- `g:deoplete#sources#padawan#server_command`

If your padawan-server bin is not in $PATH then you can set up this
to point it directly, ie: `/path/to/padawan/bin/padawan-server`.

- `g:deoplete#sources#padawan#log_file`

Padawan.php log file path, if empty log won't be stored anywhere. By default, it goes
to `/tmp/padawan-server.log` unless you have no `/tmp` directory, in that case
log won't be saved.

- `g:deoplete#sources#padawan#server_autostart`

The plugin will try to start padawan.php server automatically when completion is triggered.
Any value but `1` will make this option disabled.

## Additional commands

By default, the plugin is not creating any vim commands. However, there are some
functions available to manage the padawan.php server.

- `call deoplete#sources#padawan#StartServer()`

Will start padawan-server.

- `call deoplete#sources#padawan#StopServer()`

Will kill padawan-server.

- `call deoplete#sources#padawan#RestartServer()`

Will kill padawan-server and start it again.

### Custom commands

If you would like to have simpler commands, you can add them to your
`vimrc` file. Snippet below shows how to add `StartPadawan`, `StopPadawan` and
`RestartPadawan` commands.

```vim
command! StartPadawan call deoplete#sources#padawan#StartServer()
command! StopPadawan call deoplete#sources#padawan#StopServer()
command! RestartPadawan call deoplete#sources#padawan#RestartServer()
```

## Todo
- [x] Update configuration section
- [x] Provide actions to start and stop padawan.php server
- [ ] Add Vim help file

## Contribution

Always welcome.

## Credits

Plugin is based on [padawan.vim](https://github.com/mkusher/padawan.vim),
[deoplete-jedi](https://github.com/zchee/deoplete-jedi) and
[deoplete-go](https://github.com/zchee/deoplete-go).

## License

MIT License;
The software is provided "as is", without warranty of any kind.
