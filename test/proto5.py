import multiprocessing
import socket
from _thread import *
from multiprocessing import Process
from rplidar import RPLidar
import numpy as np
import sys
import time
import pyrebase
#import motorcontrol

HOST = '192.168.137.1'
PORT = 9999
Data = []
global left
global right
global direction_count


#car = motorcontrol.drive()
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

## 정보 받아오기
config = {
    "apiKey" : "AIzaSyCWkh7qqUThfPx9XMAtWHwImaS_b4heJmA",
    "authDomain" : "chanwhan-37aa7.firebaseapp.com",
    "databaseURL" : "https://chanwhan-37aa7.firebaseio.com/",
    "storageBucket" : "chanwhan-37aa7.appspot.com"
}

firebase = pyrebase.initialize_app(config)

db = firebase.database()

# 쓰레드에서 실행되는 코드입니다.

# 접속한 클라이언트마다 새로운 쓰레드가 생성되어 통신을 하게 됩니다.
def threaded(client_socket, addr):
    print('Connected by :', addr[0], ':', addr[1])
    copy = '0'

    # 클라이언트가 접속을 끊을 때 까지 반복합니다.
    while True:
        n = client_socket.recv(4)
        buf = n.decode()
        data = client_socket.recv(int(buf))
        if copy == data:
            continue
        else:
            copy = data
            f = open('helloClient.txt', 'w')
            f.write(data.decode())
            f.close()

    client_socket.close()

def server():
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen()

    print('server start')

    # 클라이언트가 접속하면 accept 함수에서 새로운 소켓을 리턴합니다.

    # 새로운 쓰레드에서 해당 소켓을 사용하여 통신을 하게 됩니다.
    while True:
        print('wait')

        client_socket, addr = server_socket.accept()
        start_new_thread(threaded, (client_socket, addr))

    server_socket.close()

    threading.Timer(0.1, thread_rin).start()

## 경로 안내
def infomation():
    i = 0
    path_x_list = []
    path_y_list = []

    while (1):
        lat = db.child("path").child(i).child("latitude").get()
        if (lat.val() == None):
            break
        path_x_list.append(lat.val())
        lng = db.child("path").child(i).child("longitude").get()
        path_y_list.append(lng.val())
        print(lat.val())
        print(lng.val())
        i = i + 1

    guide = db.child("guide").get()
    point = db.child("pointIndex").get()
    print(path_x_list)
    print(path_y_list)
    print(guide.val())
    print(point.val())

    x_list = list(map(float, path_x_list))
    y_list = list(map(float, path_y_list))
    direction_list = list(map(int, guide.val()))
    point_list = list(map(int, point.val()))


    guide_line = [1] * len(path_x_list)

    print(len(guide_line))
    print(len(point_list))

    for i in range(0, len(point_list)):
        guide_line[point_list[i]] = direction_list[i]

    print(guide_line)
    print(type(guide_line))

    return x_list, y_list, guide_line

def current():
    current_x = db.child("location").child("x").get()
    current_y = db.child("location").child("y").get()
    point_x = current_x.val()
    point_y = current_y.val()
    x = round(float(point_x), 5)
    y = round(float(point_y), 5)

    return x, y

def gps(l, r, c):
    x_list, y_list, guide_line = infomation()
    index = 0
    error_count = 0
    direction_count = 0
    #wheel.Forward()
    count = 0
    c.put(0)
    while (index != len(guide_line)):
        left = l.get(True, 1000)
        right = r.get(True, 1000)
        print("         left:{}\n        right:{} ".format(left,right))
        x, y = current()


        print("x: ", x)
        print("y: ", y)
        print("current index: ", index)
        print("current guide_line", guide_line[index])

        if x - round(x_list[index], 5) <= abs(0.00003) and y - round(y_list[index], 5) <= abs(0.00003):  # 3m 이내에 접근한 경우
            if guide_line[index] == 2 or (left == 0 and right > 0):
                # wheel.ZC()
                # time.sleep(1.3)
                # wheel.FForward()
                print("Turn Left")
                index += 1
            elif guide_line[index] == 3 or (left > 0 and right == 0):
                # wheel.ZD()
                # time.sleep(1.3)
                # wheel.FForward()
                print("Turn Right")
                index += 1
            elif left > 0 and right > 0:
                # wheel.Stop()
                print("Stop")
            else:
                index += 1
                # wheel.FForward()
                print("Next Index")
                error_count = 0
            # Lidar Information
        if left == 0 and right > 0:
            print("Turn Left")
            direction_count += 1
            c.put(direction_count)
            print("count: ", direction_count)
        elif left > 0 and right == 0:
            print("Turn Right")
            direction_count += 1
            c.put(direction_count)
            print("count: ", direction_count)
        elif left == 0 and right == 0:
            print("Go Straight")
            c.put(direction_count)
            direction_count = 0
            print("count: ", direction_count)
        else:
            print("Stop")
            c.put(direction_count)

        error_count += 1

        if error_count == 10000:
            # wheel.Backward()
            print("Go Back.")
            break
        if x == None:
            time.sleep(1)
            # wheel.Stop()
            print("No Direction.")
            break

    time.sleep(1)
    # wheel.Stop()
    if index == len(guide_line):
        print("Destination.")
    else:
        print("System Exit!!")



def update_line(lidar, iterator, max_degree, min_degree, max_distance, count=0):

    angle = np.array([])
    distance = np.array([])
    left = 0
    right = 0
    offsets = np.array([(np.radians(angle), distance)])
    scan = next(iterator)
    c = count
    print("디렉션 카운트: ", c)

    for sn in range(len(scan)):
        if scan[sn][1] > min_degree and scan[sn][1] < max_degree:
            if scan[sn][2] < max_distance:
                # quality = np.append(quality, scan[sn][0])
                angle = np.append(angle, scan[sn][1])
                distance = np.append(distance, scan[sn][2])
                # rad=np.array([np.radians(scan[sn][1]), scan[sn][2]])
                left, right = div_demension(scan[sn][1], left, right, c)


    return angle,distance,left,right #,rad

def div_demension(angle,left,right,count):

    if angle >= 0 and angle < (90 - count * 10):
        #print('front_right')
        right += 1
    if angle >= 90 and angle < 180:
        #print('front_left')
        pass
    if angle >= 180 and angle < 270:
        pass
    if angle >= (270 + count * 10):
        left += 1


    return left, right

def test(l, r, c):
    lidar = RPLidar(port='COM5', baudrate=115200)
    # lidar = RPLidar(port='/dev/ttyUSB0', baudrate=115200)
    iterator = lidar.iter_scans(max_buf_meas=3000)

    angle_deg = np.array([])
    distance = np.array([])
    offset = np.array([], [])

# 버퍼를 임의로 비우든지, 시간계산해서 보내든지?
    while True:
        direction_count = c.get()
        print(direction_count)
        angle_deg, distance, left, right = update_line(count=direction_count, lidar=lidar, iterator=iterator, max_degree=360, min_degree=0, max_distance=600)
        offset = np.vstack([angle_deg, distance])


        print(left)
        print(right)
        l.put(left)
        r.put(right)



if __name__=='__main__':

    l = multiprocessing.Queue()
    r = multiprocessing.Queue()
    c = multiprocessing.Queue()

    p1 = Process(target=gps, args=(l, r, c))
    p2 = Process(target=test, args=(l, r, c))

    p1.start()
    p2.start()

    p1.join()
    p2.join()