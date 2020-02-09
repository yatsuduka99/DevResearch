import time


def logger(func_name):
    def __decorator(func):
        def inner(*args, **kwargs):
            print(func_name + ":開始 " + str(time.time()))
            result = func(*args, **kwargs)
            print(func_name + ":終了 " + str(time.time()))
            return result

        return inner

    return __decorator


def calc_time(func_name=''):
    def _calc_time(func):
        import functools

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start = time.time()
            ret = func(*args, **kwargs)
            print(f'end time : {time.time() - start:0.4} sec : {func_name}')
            return ret

        return wrapper

    return _calc_time
