import time

def ratelimited(limit_qty, limit_period, iterable):
    """Return a RatelimitedIterator over iterable. Units for limit_period are in seconds."""
    return RatelimitedIterator(limit_qty, limit_period, iter(iterable))

class RatelimitedIterator(object):
    """An iterator for rate-limiting another iterator."""
    DEFAULT_CLOCK_FUNC = time.time
    DEFAULT_SLEEP_FUNC = time.sleep

    def __init__(self, limit_qty, limit_period, iterator, clock_func=None, sleep_func=None, allow_negative_sleep=False):
        """
        limit_qty is the number of times a value will be yielded within limit_period.

        limit_period is in units used by clock_func and sleep_func.

        iterator is any iterable object.

        clock_func is a function taking no arguments that retuns a Number-like value.
        sleep_func is a function taking a Number-like value that will be called when
        a delay is needed.

        In this context, "Number-like value" means an object that can be compared,
        subtracted from, divided, and added to. If clock_func and sleep_func are not
        specified, this value is in seconds.

        allow_negative_sleep allows sleep_func to be called if the desired sleep time
        is negative (eg, the last loop took longer than interval)
        """

        clock_func = clock_func or self.DEFAULT_CLOCK_FUNC
        sleep_func = sleep_func or self.DEFAULT_SLEEP_FUNC

        self.limit_qty = limit_qty
        self.limit_period = limit_period
        self.iterator = iterator
        self.clock_func = clock_func
        self.sleep_func = sleep_func
        self.allow_negative_sleep = allow_negative_sleep

        #Ensure float division (not integral division)
        self.interval = limit_period / float(limit_qty) 

        self.next_scheduled = None

    def __iter__(self):
        return self

    def next(self):
        ret = next(self.iterator) #Propagate StopIteration immediately
        self._delay()
        return ret

    def _delay(self):
        """Delay for between zero and self.interval time units"""
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
            #Call for 0, because that might be meaningful to sleep_func.
            if self.allow_negative_sleep or delay_amt >= 0: 
                self.sleep_func(self.next_scheduled - current)
