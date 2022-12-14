from queue import Queue, Empty, time, deque


class PeekQueue(Queue):
    '''
    Custom queue object with added peeking functionality.

    Create a queue object with a given maximum size.

    If maxsize is <= 0, the queue size is infinite.
    '''


    def __init__(self, data:list=None, maxsize:int=0) -> None:
        super().__init__(maxsize)
        if data is not None:
            self.queue = deque(data)


    def peek(self, block=True, timeout=None):
        """
        Returns an item from queue without removing it.

        If optional args 'block' is true and 'timeout' is None (the default),
        block if necessary until an item is available. If 'timeout' is
        a non-negative number, it blocks at most 'timeout' seconds and raises
        the Empty exception if no item was available within that time.
        Otherwise ('block' is false), return an item if one is immediately
        available, else raise the Empty exception ('timeout' is ignored
        in that case).
        """
        with self.not_empty:
            if not block:
                if not self._qsize():
                    raise Empty
            elif timeout is None:
                while not self._qsize():
                    self.not_empty.wait()
            elif timeout < 0:
                raise ValueError("'timeout' must be a non-negative number")
            else:
                endtime = time() + timeout
                while not self._qsize():
                    remaining = endtime - time()
                    if remaining <= 0.0:
                        raise Empty
                    self.not_empty.wait(remaining)
            item = self.queue[0]
            return item
