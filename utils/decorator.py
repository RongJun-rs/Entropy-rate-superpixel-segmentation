import time,pdb,functools
import numpy as np
def debugit(function):
    '''Decorator that places a break point right before calling the function.'''
    @functools.wraps(function)
    def debug_mode(*args, **kwargs):
        return pdb.runcall(function,*args, **kwargs)
    return debug_mode
def timeit(nbtimes=1,deactivate=False,show_mean_duration_only=True):
    def decorator(func):
        if deactivate:
            return func
        @functools.wraps(func)
        def time_mode(*args,**kwargs):
            deltas = []
            for i in range(nbtimes):
                start = time.time()
                res = func(*args,**kwargs)
                stop =time.time()
                if not(show_mean_duration_only):
                    print(f"duration of {func.__name__} is {stop-start}" )
                deltas.append(stop-start)
            print(f"mean duration of {func.__name__} is {np.mean(deltas)} repeated {nbtimes}")
            return res
        return time_mode
    return decorator
