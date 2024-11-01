


class RetryContextDecorator:
    def __init__(self, tries, backoff, exceptions):
        pass


    def __enter__(self, ...):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def __call__(self, func):   #*args, **kwargs):

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            with self:
                return func(*args, **kwargs)
        return wrapper




    def _foo(self):
        for try_num in range(n_tries):

            if try_num > 0:
                sleep_time = backoff_f(try_num-1)
                total_sleep += sleep_time
                sleep_f(sleep_time)

            try:
                return func(*args, **kwargs)
            except exc as e:
                exception_list.append(e)

        raise GiveUp(try_num+1, total_sleep, func, exception_list)
