import threading
import multiprocessing
import random
import time
import os

cc = time.time()


def write(name):
    print(os.getpid(), os.getppid())
    c = time.time()
    a = ''.join([chr(random.randint(0, 100)) for _ in range(1000000)])
    a = a.encode()
    with open("%s.txt" % name, 'wb') as ff:
        ff.write(a)
        print(name, 'done')
    print(time.time() - c)


for x in range(3):
    t = threading.Thread(target=write, args=(x,))
    t.daemon = True
    t.start()


# if __name__ == '__main__':
#     with multiprocessing.Pool(5) as p:
        # p.map(write, [1, 2, 3])
    # print('total', time.time() - cc)

print('total', time.time() - cc)
