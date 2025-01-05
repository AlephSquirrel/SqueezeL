import argparse, sys

CHARS = ' "()0123456789abcdefghijklmnopqrstuvwxyz'

def unpack(filename):
    if filename[-5:] != '.sqzl':
        sys.stderr.write("Error: File extension must be .sqzl")
        sys.exit(1)
    try:
        f = open(filename, 'rb')
        binary = f.read()
        f.close()
    except IOError:
        sys.stderr.write("Error: Can't open file '%s'" % filename)
        sys.exit(1)
    
    prgm = ''
    next_val = 0
    num_bytes = 0
    
    for b in binary:
        next_val = (next_val << 8) + b
        num_bytes += 1
        if num_bytes % 2 == 0:
            prgm += CHARS[next_val // 1600] + CHARS[next_val // 40 % 40] + CHARS[next_val % 40]
            next_val = 0
    
    if num_bytes % 2 == 1:
        prgm += CHARS[next_val]
    
    return prgm

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Unpack and display the contents of a SqueezeL program')
    parser.add_argument('prgm', metavar='prgm.sqzl', type=str,
                        help='the .sqzl to unpack')
    args = parser.parse_args()

    print(unpack(args.prgm))