import sys
sys.dont_write_bytecode = True
from time import time
from queue import Queue


class TimeoutableQueue(Queue):
    def join_with_timeout(self, timeout):
        self.all_tasks_done.acquire()
        # try:
        endtime = time() + timeout
        while self.unfinished_tasks:
            remaining = endtime - time()
            if remaining <= 0.:
                raise Exception
            self.all_tasks_done.wait(remaining)
        # finally:
        #     self.all_tasks_done.release()