import functools, itertools, math

PI = math.pi

def factorial(*args):
    '''
    Factorial / Permutations
    
    (zmf num)      num!
    (zmf list/str) List of permutations of list/str
    '''
    if isinstance(args[0], int):
        return math.factorial(args[0])
    elif isinstance(args[0], float):
        return math.gamma(args[0] + 1)
    elif isinstance(args[0], list):
        return [list(x) for x in itertools.permutations(args[0])]
    elif isinstance(args[0], str):
        return [''.join(x) for x in itertools.permutations(args[0])]
    else:
        raise ValueError

def gcd(*args):
    '''
    GCD
    
    (zmg num*) GCD of nums
    '''
    return functools.reduce(math.gcd, args, 0)

def lcm(*args):
    '''
    LCM
    
    (zml num*) LCM of nums
    '''
    return functools.reduce(math.lcm, args, 1)

def log(*args):
    '''
    Logarithm
    
    (zmn num [base]) Logarithm of num to base (e by default)
    '''
    return math.log(*args)

def sqrt(*args):
    '''
    Square Root
    
    (zms num) Square root of num
    '''
    return math.sqrt(args[0])

def trig(*args):
    '''
    Trig Functions
    
    (zmt idx num [num2])
    
    Computes a trig function of num, selected based on idx.
    idx = 0: radians -> degrees
    idx = 1: sin
    idx = 2: cos
    idx = 3: tan
    idx = 4: degrees -> radians
    idx = 5: asin
    idx = 6: acos
    idx = 7: atan (with optional 2nd argument)
    '''
    if args[0] == 7 and len(args) == 3:
        return math.atan2(args[1], args[2])
    else:
        return [math.degrees, math.sin, math.cos, math.tan, math.radians, math.asin, math.acos, math.atan][args[0]](args[1])
