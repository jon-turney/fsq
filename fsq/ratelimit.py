import time

def ratelimited(limit_qty, limit_period, iterable):
    """Return a RatelimitedIterator over iterable. Units for limit_period are in seconds."""
    return RatelimitedIterator(limit_qty, limit_period, iter(iterable))

class RatelimitedIterator(object):
    """An iterator for rate-limiting another iterator.

       limit_qty is the number of times a value will be yeilded within limit_period.

       limit_period is in units used by clock_func and sleep_func.

       clock_func is a function taking no arguments that retuns a Number-like value.
       sleep_func is a function taking a Number-like value that will be called when
       a delay is needed.

       In this context, "Number-like value" means an object that can be compared,
       subtracted from, divided, and added to. If clock_func and sleep_func are not
       specified, this value is in seconds.
       """

    def __init__(self, limit_qty, limit_period, iterator, clock_func=None, sleep_func=None, allow_negative_sleep=False):
        if not clock_func:
            clock_func = time.time
        if not sleep_func:
            sleep_func = time.sleep

        self.limit_qty = limit_qty
        self.limit_period = limit_period
        self.iterator = iterator
        self.clock_func = clock_func
        self.sleep_func = sleep_func
        self.allow_negative_sleep = allow_negative_sleep

        self.interval = limit_period / float(limit_qty) #Float division

        self.next_scheduled = None

    def __iter__(self):
        return self

    def next(self):
        ret = next(self.iterator) #Propagate StopIteration immediately
        self._delay()
        return ret

    def _delay(self):
        if not self.next_scheduled:
            self.next_scheduled = self.clock_func() + self.interval
            return
        while True:
            current = self.clock_func()
            if current >= self.next_scheduled:
                extratime = current - self.next_scheduled
                self.next_scheduled = current + self.interval - extratime
                return
            delay_amt = self.next_scheduled - current
            if self.allow_negative_sleep or delay_amt >= 0: #Call for 0, because that might be meaningful to sleep_func.
                self.sleep_func(self.next_scheduled - current)
