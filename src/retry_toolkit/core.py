import functools



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
                self._execute_with_retry(func, *args, **kwargs)
        return wrapper


    def _execute_with_retry(self, func, *args, **kwargs):
        self._setup()

        for try_num in range(self.n_tries):
            self._sleep(try_num)
            try:
                return func(*args, **kwargs)
            except excs_to_catch as e:
                self._exception(e)

        self._giveup()


    def _setup(self):
        # configure at call-time to allow any changes to defaults
        # to properly take effect each time func is used
        n_tries_f = _ensure_callable(tries      , Defaults.TRIES  )
        backoff_f = _ensure_callable(backoff    , Defaults.BACKOFF)
        exc_f     = _ensure_callable(exceptions , Defaults.EXC    )
        sleep_f   = Defaults.SLEEP_FUNC

        n_tries = n_tries_f()
        exc     = exc_f()

        # context/state
        total_sleep    = 0.0
        exception_list = []


    def _sleep(self, try_num):
        if try_num > 0:
            sleep_time = backoff_f(try_num-1)
            total_sleep += sleep_time
            sleep_f(sleep_time)


    def _exception(self, e):
        exception_list.append(e)


    def _giveup(self):
        raise GiveUp(try_num+1, total_sleep, func, exception_list)






    def _foo(self):
        for try_num in range(n_tries):


            try:
                return func(*args, **kwargs)
            except exc as e:

        raise GiveUp(try_num+1, total_sleep, func, exception_list)
