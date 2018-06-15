from threading import Thread, Lock
from random import randint
import time
import sys

def delay():
    time.sleep(randint(0, 1))

class MyThread(Thread):
    def __init__(self, position, chops):
        Thread.__init__(self)
        self.position = position
        self.chops = chops

    def run(self):
        t_end = time.time() + 10
        while time.time() < t_end:
            print("philosopher " + repr(self.position) + " is thinking")
            delay()
            print("philosopher " + repr(self.position) + " is hungry")
            if (self.position % 2 == 2):
                self.chops[self.position].acquire()
                self.chops[(self.position + 4) % 5].acquire()
                print("philosopher " + repr(self.position) + " is eating")
                delay()
                print("philosopher " + repr(self.position) + " finished eating")
                self.chops[self.position].release()
                self.chops[(self.position + 4) % 5].release()
            else:
                self.chops[(self.position + 4) % 5].acquire()
                self.chops[self.position].acquire()
                print("philosopher " + repr(self.position) + " is eating")
                delay()
                print("philosopher " + repr(self.position) + " finished eating")
                self.chops[(self.position + 4) % 5].release()
                self.chops[self.position].release()

import ctypes

def terminate_thread(thread):
    """Terminates a python thread from another thread.

    :param thread: a threading.Thread instance
    """
    if not thread.isAlive():
        return

    exc = ctypes.py_object(SystemExit)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(
        ctypes.c_long(thread.ident), exc)
    if res == 0:
        raise ValueError("nonexistent thread id")
    elif res > 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(thread.ident, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")

def main():
    step = 0
    chops = [Lock() for count in range(5)]
    threads = [MyThread(count, chops) for count in range(5)]
    for count in range(5):
        threads[count].start()
    time.sleep(5)
    # for count in range(5):
    #     terminate_thread(threads[count])

if __name__ == "__main__":
    main()

