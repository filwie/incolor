# incolor
## Description
Very simple package that aims at adding some color to Your life.

## Quickstart
- Add color codes to text (uses color numbers)
``` python
>>> from incolor import incolor
>>> incolor('I\'m blue da ba dee', fg=4)
"\x1b[34mI'm blue da ba dee\x1b[0m"
```

- Add color codes to text (uses color names)
``` python
>>> from incolor import incolor, Color
>>> incolor('I\'m blue da ba dee', fg=Color.blue)
"\x1b[34mI'm blue da ba dee\x1b[0m"
```

- Join multiple arguments in colorful manner
``` python
>>> incolor('First', 2, 'third', list(), fg=Color.brightwhite)
'\x1b[315mFirst 2 third []\x1b[0m'
```

- Color print function (behaves exactly like `print(incolor(...))`)
``` python
>>> cprint('Yellow: 🚢', 123, 'yay', fg=3)
Yellow: 🚢 123 yay
```

- Both functions accept `sep` argument
```python
>>> incolor(0, 'a', 1, 2, sep='\t')
'\x1b[30ma\t1\t2\x1b[0m'
>>> cprint(0, 'a', 1, 2, sep='\t')
a       1       2
```

## Tests

To run tests execute `test.sh` script
``` sh
./test.sh
```

Prerequisites:
- docker
- Internet connection 😃

## #TODO
- [x] add colors only if output is a TTY
- [x] verify Windows support (probably not working?)
- [x] add more ways to specify colors (f.e. from string: `'red'`)
- [ ] add support for `256 colors`
- [x] add support for `Truecolor`
