import functools, itertools, operator, sys

def errprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def vectorize(f):
    vf = lambda *args: f(*args) if not any(isinstance(x, list) for x in args) else list(
        map(vf, *[x if isinstance(x, list) else itertools.repeat(x) for x in args]))
    vf.__doc__ = f.__doc__
    return vf

@vectorize
def add(*args):
    '''
    Add (vectorized)
    
    (a num*) Sum of nums
    '''
    if any(isinstance(x, str) for x in args): raise ValueError
    return sum(args)

@vectorize
def subtract(*args):
    '''
    Subtract / Negate (vectorized)
    
    (s num)                -num
    (s num1 num2 ... numk) num1 - num2 - ... - numk
    '''
    if any(isinstance(x, str) for x in args): raise ValueError
    if len(args) == 0: return 0
    elif len(args) == 1: return -args[0]
    else: return args[0] - sum(args[1:])

@vectorize
def multiply(*args):
    '''
    Multiply / Repeat String (vectorized)
    
    (m num*)    Product of nums
    (m str num) str repeated num times
    '''
    if len(args) == 2 and isinstance(args[0], str) and isinstance(args[1], int):
        return args[0] * args[1]
    elif any(isinstance(x, str) for x in args): raise ValueError
    return functools.reduce(operator.mul, args, 1)

@vectorize
def divide(*args):
    '''
    Divide / Reciprocal / Split String (vectorized)
    
    (d num)                1 / num
    (d num1 num2 ... numk) num1 / num2 / ... / numk
    (d str [sep])          Split str by sep (space if not specified)
    '''
    if len(args) == 0: return 1
    elif isinstance(args[0], (int, float, complex)):
        if len(args) == 1: result = 1 / args[0]
        else: result = functools.reduce(operator.truediv, args)
        if isinstance(result, float) and result.is_integer(): result = int(result)
        return result
    else:
        if len(args) == 1: return args[0].split(' ')
        elif args[1] == '': return list(args[0])
        else: return args[0].split(args[1])

@vectorize
def modulo(*args):
    '''
    Modulo / Parity (vectorized)
    
    (r num)                num % 2
    (r num1 num2 ... numk) num1 % num2 % ... % numk
    '''
    if any(isinstance(x, str) for x in args): raise ValueError
    if len(args) == 0: return 0
    elif len(args) == 1: return args[0] % 2
    else: return functools.reduce(operator.mod, args)

def power(*args):
    '''
    Power / Apply
    
    (p num1 num2)      num1 ** num2
    (p func list)      Call func with list as its arguments.
    '''
    if callable(args[0]):
        return args[0](*args[1])
    else:
        return args[0] ** args[1]

def equal(*args):
    '''
    Equal
    
    Returns 1 if all arguments are equal, 0 otherwise.
    '''
    return int(all(args[i] == args[i+1] for i in range(len(args)-1)))

def greater_than(*args):
    '''
    Greater Than
    
    Returns 1 if arguments are in strictly descending order, 0 otherwise.
    '''
    return int(all(args[i] > args[i+1] for i in range(len(args)-1)))

def parse_number(*args):
    '''
    Parse Number / Bitwise Not
    
    (zn str [base])
    (zn list [base])
    
    str interpreted as a number, or list interpreted as the digits of a number.
    base is 10 by default. It cannot be provided if the first argument is a string representing a float or complex number.
    
    (zn num)        ~num
    '''
    if isinstance(args[0], str):
        try:
            return int(*args)
        except:
            try:
                return float(args[0])
            except:
                try:
                    return complex(args[0])
                except:
                    errprint(f"Invalid numeric literal: {args[0]}")
                    exit(1)
    elif isinstance(args[0], list):
        if len(args) == 1:
            return functools.reduce((lambda x,y: 10*x+y), args[0])
        else:
            return functools.reduce((lambda x,y: args[1]*x+y), args[0])
    else:
        return ~args[0]

@vectorize
def bitwise_and(*args):
    '''
    Bitwise And (vectorized)
    
    (za num1 num2 ... numk) num1 & num2 & ... & numk
    '''
    if any(isinstance(x, str) for x in args): raise ValueError
    return functools.reduce(operator.and_, args, -1)

@vectorize
def bitwise_or(*args):
    '''
    Bitwise Inclusive Or (vectorized)
    
    (zi num1 num2 ... numk) num1 | num2 | ... | numk
    '''
    if any(isinstance(x, str) for x in args): raise ValueError
    return functools.reduce(operator.or_, args, 0)

@vectorize
def bitwise_xor(*args):
    '''
    Bitwise Exclusive Or (vectorized)
    
    (zx num1 num2 ... numk) num1 ^ num2 ^ ... ^ numk
    '''
    if any(isinstance(x, str) for x in args): raise ValueError
    return functools.reduce(operator.xor, args, 0)

@vectorize
def bitshift(*args):
    '''
    Bit Shift (vectorized)
    
    (zh num1 num2)
    If num2 >= 0: num1 << num2
    If num2 < 0:  num1 >> -num2
    '''
    return (args[0] << args[1]) if args[1] >= 0 else (args[0] >> -args[1])

def minimum(*args):
    '''
    Minimum
    
    Returns smallest argument.
    '''
    return min(args)

def maximum(*args):
    '''
    Maximum
    
    Returns largest argument.
    '''
    return max(args)

def floor(*args):
    '''
    Floor
    
    (zf num)       floor(num)
    (zf num1 num2) floor(num1 / num2)
    (zf str)       str lowercased
    '''
    if isinstance(args[0], (int, float)):
        if len(args) == 1:
            return int(args[0])
        else:
            return int(args[0] / args[1])
    elif isinstance(args[0], str):
        return args[0].lower()
    else:
        raise ValueError

def ceiling(*args):
    '''
    Ceiling
    
    (zc num)       ceil(num)
    (zc num1 num2) ceil(num1 / num2)
    (zc str)       str uppercased
    '''
    if isinstance(args[0], (int, float)):
        if len(args) == 1:
            return int(args[0])
        else:
            return int(args[0] / args[1])
    elif isinstance(args[0], str):
        return args[0].upper()
    else:
        raise ValueError

def abs_val(*args):
    '''
    Absolute Value
    
    (zv num) Absolute value of num
    '''
    return abs(args[0])

def contains(*args):
    '''
    Any / Contains
    
    (y list [a])
    
    Returns 1 if any element of the list is truthy, 0 otherwise.
    If a is a number, string, or list, tests if list contains a.
    If a is a function, tests if a returns a truthy value on any element of list.
    '''
    
    L = args[0]
    if len(args) == 1:
        return int(any(L))
    elif callable(args[1]):
        return int(any(args[1](x) for x in L))
    else:
        return int(args[1] in L)

def iota(*args):
    '''
    Range / Length
    
    (b end)              [0 ... end-1]
    (b start end [step]) Sequence of numbers from start (inclusive) to end (exclusive), with step size step (1 if unspecified)
    (b list/str)         Length of list/str
    '''
    if isinstance(args[0], (list, str)):
        return len(args[0])
    else:
        return list(range(*args))

def make_list(*args):
    '''
    List
    
    Returns a list containing its arguments.
    '''
    return list(args)

def map_list(*args):
    '''
    Map / Char <-> Code
    
    (k func list*) Maps func onto list(s)
    (k char)       ord(char)
    (k num)        chr(num)
    '''
    if callable(args[0]):
        func, *lists = args
        return list(map(func, *lists))
    elif isinstance(args[0], str):
        return ord(args[0])
    else:
        return chr(args[0])

def concatenate(*args):
    '''
    Concatenate
    
    (c item*)
    Concatenates together items. If at least one parameter is a list, the result will be a list. Otherwise, the result will be a string.
    '''
    if any(isinstance(x, list) for x in args):
        return list(itertools.chain(*[x if isinstance(x, list) else [x] for x in args]))
    else:
        return ''.join(str(x) for x in args)

def join(*args):
    '''
    Join / Reduce
    
    (j str list)  Joins together elements of list with separator str.
    (j func list) Apply func (a 2 argument function) to elements of list left to right, reducing to a single result.
    '''
    if callable(args[0]):
        return functools.reduce(args[0], args[1])
    else:
        return args[0].join(str(x) for x in args[1])

def position(*args):
    '''
    Position
    
    (zp list a)
    If a is a number, list, or string, returns the index of the first occurence of a in list (or -1 if it does not appear).
    If a is a function, returns the index of the first element for which a returns a truthy value (or -1 if there is none).
    '''
    if not isinstance(args[0], list): raise ValueError
    if callable(args[1]):
        test = args[1]
    else:
        test = lambda x: x == args[1]
    for i,e in enumerate(args[0]):
        if test(e): return i
    return -1

def reverse(*args):
    '''
    Reverse
    
    (zr list/str) Reverse list/str
    '''
    return args[0][::-1]

def sort(*args):
    '''
    Sort
    
    (zt list/str [func])
    Sort list/str. If func is provided, it is used as the sorting key.
    '''
    if len(args) == 1:
        result = sorted(args[0])
    else:
        result = sorted(args[0], key=args[1])
    if isinstance(args[0], str):
        result = ''.join(result)
    return result

def uniquify(*args):
    '''
    Uniquify
    
    (zu list/str)
    Deduplicates elements/characters of list/str. Original order is preserved.
    '''
    if isinstance(args[0], list):
        result = []
        for x in args[0]:
            if x not in result: result.append(x)
    else:
        result = ''
        for c in args[0]:
            if c not in result: result += c
    return result

def head(*args):
    '''
    Head / Element / Increment
    
    (h list)     list[0]
    (h list idx) list[idx]
    (h num)      num + 1
    '''
    if isinstance(args[0], (list, str)):
        if len(args) == 1:
            return args[0][0]
        else:
            return args[0][args[1]]
    else:
        return args[0] + 1

def tail(*args):
    '''
    Tail / Subsequence / Filter / Decrement
    
    (t list)                list[1:]
    (t list start)          list[start:]
    (t list start end)      list[start:end]
    (t list start end step) list[start:end:step]
    (t list func)           List of elements of list for which func returns truthy
    (t num)                 num - 1
    '''
    if isinstance(args[0], (list, str)):
        if len(args) == 1:
            return args[0][1:]
        elif len(args) == 2:
            if callable(args[1]):
                return list(filter(args[1], args[0]))
            else:
                return args[0][args[1]:]
        else:
            return args[0][slice(*args[1:])]
    else:
        return args[0] - 1

def get_input(*args):
    '''
    Input
    
    (i) Get a line of user input.
    '''
    return input()

def output(*args):
    '''
    Output
    
    (o item*) Print items separated by spaces, with a trailing newline.
    '''
    print(*args)

def output_ww(*args):
    '''
    Output without whitespace
    
    (zw item*) Print items with no separator or trailing newline.
    '''
    print(*args, sep='', end='')

def exit_repl(*args):
    '''
    Exit REPL / Default parameter
    
    Type (x) to exit the REPL. x is also used as the default parameter for lambdas.
    '''
    exit()