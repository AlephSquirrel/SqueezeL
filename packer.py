import argparse, sys

CHARS = ' "()0123456789abcdefghijklmnopqrstuvwxyz'

def pack(filename):
    try:
        f = open(filename, 'r')
        prgm = f.read()
        f.close()
    except IOError:
        sys.stderr.write("Error: Can't open file '%s'" % filename)
        sys.exit(1)
    
    if len(prgm) % 3 == 2: prgm = " " + prgm
    
    byte_arr = []
    next_val = 0
    chars = 0
    
    for c in prgm:
        idx = CHARS.find(c.lower())
        if idx == -1: continue
        next_val = 40 * next_val + idx
        chars += 1
        
        if chars % 3 == 0:
            byte_arr += [next_val >> 8, next_val & 255]
            next_val = 0
    
    if chars % 3 == 1:
        byte_arr += [next_val]
    
    fileout = filename.rsplit(".",1)[0] + '.sqzl'
    try:
        f = open(fileout, 'wb')
        f.write(bytearray(byte_arr))
        f.close()
    except IOError:
        sys.stderr.write("Error: Can't open file '%s'" % fileout)
        sys.exit(1)

parser = argparse.ArgumentParser(description='Pack a SqueezeL program')
parser.add_argument('prgm', metavar='prgm', type=str,
                    help='the filename of the SqueezeL source code to pack')
args = parser.parse_args()

pack(args.prgm)