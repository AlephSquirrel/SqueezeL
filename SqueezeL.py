import argparse, re, sys, unpacker
from std_ops import *
from math_ops import *
from other_ops import *
from string_ops import *

class Env(dict):
    "An environment: a dict of {'var': val} pairs, with an outer Env."
    def __init__(self, params=(), args=(), outer=None):
        self.update(zip(params, args))
        self.outer = outer
    def find(self, var):
        "Find the innermost Env where var appears."
        return self if (var in self) else (None if self.outer is None else self.outer.find(var))

def standard_env() -> Env:
    "An enviroment with some standard procedures."
    env = Env()
    env.update({
        'a': add,
        'b': iota,
        'c': concatenate,
        'd': divide,
        'e': equal,
        'f': 0,
        'g': greater_than,
        'h': head,
        'i': get_input,
        'j': join,
        'k': map_list,
        'l': make_list,
        'm': multiply,
        'n': '\n',
        'o': output,
        'p': power,
        'r': modulo,
        's': subtract,
        't': tail,
        'u': '',
        'v': [],
        'w': ' ',
        'x': exit_repl,
        'y': contains,
        'z0': minimum,
        'z9': maximum,
        'za': bitwise_and,
        'zc': ceiling,
        'zf': floor,
        'zh': bitshift,
        'zi': bitwise_or,
        'zn': parse_number,
        'zr': reverse,
        'zp': position,
        'zt': sort,
        'zu': uniquify,
        'zv': abs_val,
        'zw': output_ww,
        'zx': bitwise_xor,
        'zmf': factorial,
        'zmg': gcd,
        'zml': lcm,
        'zmn': log,
        'zmp': PI,
        'zms': sqrt,
        'zmt': trig,
        'zor': randomness,
        'zsr': replace,
    })
    return env

global_env = standard_env()

class Procedure(object):
    "A callable function defined at runtime."
    def __init__(self, params, body, env):
        self.params, self.body, self.env = params, body, env
    def __call__(self, *args):
        proc_env = Env(self.params, args, self.env)
        for statement in self.body:
            result = leval(statement, proc_env)
        return result

def leval(x, env=global_env):
    "Evaluate an expression in an environment."
    if x is None: return None
    if isinstance(x, str):
        if x[0] == '"':
            return parseString(x)
        else:
            scope = env.find(x)
            if scope is None:
                errprint(f"Unknown symbol: {x}")
                exit(1)
            return scope[x]
    elif not isinstance(x, list):
        return x
    op, *args = x
    if op == 'u':      # for
        iter_form, *body = args
        symbol, *exps = iter_form
        exp_vals = [leval(x, env) for x in exps]
        if isinstance(exp_vals[0], (list, str)):
            iterator = iter(exp_vals[0])
        else:
            iterator = range(*exp_vals)
        for iter_val in iterator:
            env[symbol] = iter_val
            for statement in body: leval(statement, env)
        return None
    elif op == 'v':      # if/cond
        for i in range(0, len(args)-1, 2):
            test = args[i]
            if leval(test, env):
                return leval(args[i+1], env)
        else:
            return leval(args[-1], env) if len(args)%2==1 else 0
    elif op == 'w':      # while
        test, *body = args
        while leval(test, env):
            for statement in body: leval(statement, env)
        return None
    elif op == 'n':      # assignment
        symbols = args[::2]
        exps = args[1::2]
        vals = [leval(exp, env) for exp in exps]
        for symbol, val in zip(symbols, vals):
            scope = env.find(symbol)
            if scope is not None:
                scope[symbol] = val
            else:
                env[symbol] = val
        return vals[-1]
    elif op == 'f':      # lambda
        if len(args) <= 1 or not all(isinstance(x, str) for x in args[0]):
            params = ['x']
            body = args
        else:
            params, *body = args
        return Procedure(params, body, env)
    else:
        proc = leval(op, env)
        vals = [leval(arg, env) for arg in args]
        return proc(*vals)

def parseString(s):
    s = s[1:]
    if s.endswith('"'): s=s[:-1]
    result = ''
    while s:
        nextSeq = re.match(r'^\(\(|^\)\)|^\)"|^\)[a-z]|^\)\d[0-9a-z]|^\([0-9a-z]{4}|^.', s)
        seqLength = nextSeq.end()
        seq = nextSeq.group()
        if seq == '((':                          result += '('
        elif seq == '))':                        result += ')'
        elif seq == ')"':                        result += '"'
        elif seq[0] == ')' and seq[1].isalpha(): result += seq[1].upper()
        elif seq[0] in '()':                     result += chr(int(seq[1:], 36))
        else:                                    result += seq
        s = s[seqLength:]
    return result

def tokenize(s):
    tokens = []
    s = s.lstrip()
    while s:
        nextToken = re.match(r'^\d+|^[a-y]|^z[mos]?[0-9a-z]|^"(\)"|[^"])*"?|^.', s)
        tokenLength = nextToken.end()
        tokens.append(nextToken.group())
        s = s[tokenLength:].lstrip()
    return tokens

def read_from_tokens(tokens):
    if len(tokens) == 0:
        return None
    token = tokens.pop(0)
    if token == "(":
        L = []
        while len(tokens) > 0 and tokens[0] != ")":
            L.append(read_from_tokens(tokens))
        if len(tokens) > 0: tokens.pop(0)
        return L
    elif token == ")":
        errprint("Unexpected )")
        exit(1)
    elif token[0].isalpha():
        return token
    elif token[0] == '"':
        return token
    else:
        return parse_number(token)

def repl():
    "A read-eval-print loop."
    print("  _______(0.0)\n_/SqueezeL/\n V V   V V")
    while True:
        val = leval(read_from_tokens(tokenize(input("> "))))
        if val is not None:
            if callable(val):
                print(val.__doc__)
            else:
                print(val)

parser = argparse.ArgumentParser(
    prog='SqueezeL',
    description='Runs a SqueezeL program.'
)
parser.add_argument('prgm', metavar='prgm.sqzl', type=str, nargs='?',
                    help='The .sqzl file to run. If none is specified, the REPL is started.')
args = parser.parse_args()

if args.prgm is None:
    repl()
else:
    tokens = tokenize(unpacker.unpack(args.prgm))
    val = None
    while tokens:
        val = leval(read_from_tokens(tokens))
        if val is not None: print(val) # Implicit print