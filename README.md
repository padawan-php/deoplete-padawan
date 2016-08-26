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

Plugin requires no configuration, however, it is possible to change some options.

Comming soon(tm)

## Todo
- [ ] Update configuration section
- [ ] Add Vim help file
- [ ] Provide actions to start and stop padawan.php server

## Contribution

Always welcome.

## Credits

Plugin is based on [padawan.vim](https://github.com/mkusher/padawan.vim),
[deoplete-jedi](https://github.com/zchee/deoplete-jedi) and
[deoplete-go](https://github.com/zchee/deoplete-go).

## License

MIT License;
The software is provided "as is", without warranty of any kind.
