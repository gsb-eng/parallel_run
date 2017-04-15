"""
Module to hold the services required for api hits
"""


import time
import threading

try:
    from Queue import Empty, Queue
except ImportError:
    from queue import Empty, Queue


class Worker(threading.Thread):
    """
    Worker builder and operator

    Each worker is a thread, which is having one input queue and output queue
    linked.

    This should act like a daemon, should read the input from input queue
    and send the output to the output queue.
    """

    def __init__(self, in_q, out_q):

        super(Worker, self).__init__()

        # Input queue for the worker
        self.in_q = in_q
        # Output queue for the worker
        self.out_q = out_q

    def run(self):
        # This will run forever, until a queue is empty.
        while 1:
            try:
                # get the task for action to be taked
                request = self.in_q.get(timeout=1)
            except Empty:
                break
            else:
                # request should have implemented fire method to send request
                # and process the response. The result should be added to out
                # queue
                self.out_q.put(request.fire())
                break


class WorkerManager(object):

    def __init__(self, requests, worker_count=3):
        self.requests = requests
        self.worker_count = worker_count

        self.in_q, self.out_q = Queue(), Queue()

        for req in self.requests:
            self.in_q.put(req)

    def __initiate_workers(self):
        """Method to initiate workers"""
        
        for _ in range(self.worker_count):   
            worker = Worker(self.in_q, self.out_q)
            worker.start()

    def __read_out_q(self):
        """Method to read the out queue"""
        out_put = []
        while len(out_put) != len(self.requests):
            try:
                out_put.append(
                    self.out_q.get(timeout=1)
                )
            except Empty:
                pass

        return out_put

    def distribute(self):
        """Method to distribute work load to workers"""
        self.__initiate_workers()
        return self.__read_out_q()
