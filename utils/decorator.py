import time,pdb,functools

def debugit(function):
    '''Decorator that places a break point right before calling the function.'''
    @functools.wraps(function)
    def debug_mode(*args, **kwargs):
        return pdb.runcall(function,*args, **kwargs)
    return debug_mode

def timeit(func):
    @functools.wraps(func)
    def time_mode(*args,**kwargs):
        start = time.time()
        res = func(*args,**kwargs)
        stop =time.time()
        print(f"duration of {func.__name__} is {stop-start}" )
        return res
    return time_mode
