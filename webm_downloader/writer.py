import threading
import time

# Define a function for the thread


def print_time(threadName, delay):
    print(threadName)

    with open(threadName + '.txt', 'w') as f:
        f.write(threadName)

# Create two threads as follows
try:
    t = threading.Thread(target=print_time, args=('Thread_1', 0))
    t1 = threading.Thread(target=print_time, args=('Thread_2', 5))
    t.run()
    t1.run()
except BaseException as e:
    print("Error: %s" % e)

# while 1:
#     pass
