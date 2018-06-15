from threading import Thread, Lock
from random import randint
import time
from shutil import copy2


def delay():
    time.sleep(randint(0, 2))


x = Lock()
wsem = Lock()

reader = 0

class Reader(Thread):
    def __init__(self, position):
        Thread.__init__(self)
        self.position = position

    def run(self):
        global reader
        x.acquire()
        reader = reader + 1
        if reader == 1:
            wsem.acquire()
        x.release()
        delay()
        # reading
        print("reader " + repr(self.position) + " is reading")
        copy2("payload.txt", "reader"+repr(self.position)+".txt")
        # print("reader " + repr(self.position) + "is reading")
        x.acquire()
        reader = reader - 1
        if reader == 0:
            wsem.release()
        x.release()


class Writer(Thread):
    def __init__(self, position):
        Thread.__init__(self)
        self.position = position

    def run(self):
        delay()
        with open("writer" + repr(self.position) + ".txt") as file:
            for line in file:
                wsem.acquire()
                with open("payload.txt","a") as payload:
                    print("writer "+repr(self.position)+" is writing")
                    payload.write(line)
                    payload.close()
                # write file
                # delay()
                wsem.release()
            file.close()

def main():
    for count in range(5):
        writer = Writer(count)
        writer.start()
    for count in range(10):
        reader = Reader(count)
        reader.start()
    # time.sleep(30)
    return 0


import ctypes


if __name__ == "__main__":
    main()
