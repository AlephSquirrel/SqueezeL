import random

def randomness(*args):
    '''
    Random
    
    (zor)           Random float in [0, 1)
    (zor end)       Random int in [0 ... end-1]
    (zor start end) Random int in [start ... end-1]
    (zor list/str)  Random element/char of list/str
    '''
    if len(args) == 0:
        return random.random()
    elif isinstance(args[0], int):
        return random.randrange(*args)
    elif isinstance(args[0], (list, str)):
        return random.choice(args[0])