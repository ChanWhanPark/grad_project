import multiprocessing as mp
import time
start = time.time()


def pt1(left,right):
    x = 0
    y = 0
    while True:
        x += 1
        y += 1
        left.put(x)
        right.put(y)
        print('2. left = {0}\n right ={1}'.format(x, y))




def pt2(left,right):
    while True:
        x =left.get()
        y =right.get()
        print('                             1. left = {0}\n right ={1}'.format(x,y))

if __name__=='__main__':

    left =mp.Queue()
    right =mp.Queue()

    p2 = mp.Process(target=pt1,args=[left,right])
    p1 = mp.Process(target=pt2,args=[left,right])

    p1.start()
    p2.start()

    p1.join()
    p2.join()