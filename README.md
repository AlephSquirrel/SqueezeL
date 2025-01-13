# SqueezeL
SqueezeL is a golfing language with Lisp-like syntax and a 40-character codepage. This means that 3 characters can be packed into 2 bytes, since 40³<256². If your source code is `n` characters long, it will be `ceil(n * 2/3)` bytes after packing.

SqueezeL is currently in alpha. I'm still working on adding more features, complete documentation, etc.

## Usage
To open an interactive REPL, simply run the main file:
`python3 SqueezeL.py`

In the REPL, you can type the name of a function to learn more about it.

Run a program like this:
`python3 SqueezeL.py prgm.sqzl`

The program needs to be a .sqzl file, which is created using the packer:
`python3 packer.py prgm.txt`
## License
This project is licensed under the MIT License. Parts of `SqueezeL.py` are based on [lis.py](https://github.com/norvig/pytudes/blob/main/py/lis.py), which was created by Peter Norvig and also published under the MIT License.
