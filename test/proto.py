from rplidar import RPLidar
import numpy as np
#import control
import time
import pyrebase



## 정보 받아오기
config = {
    "apiKey" : "AIzaSyCWkh7qqUThfPx9XMAtWHwImaS_b4heJmA",
    "authDomain" : "chanwhan-37aa7.firebaseapp.com",
    "databaseURL" : "https://chanwhan-37aa7.firebaseio.com/",
    "storageBucket" : "chanwhan-37aa7.appspot.com"
}

firebase = pyrebase.initialize_app(config)

db = firebase.database()

div = 1

def infomation():
    i = 0
    path_x_list = []
    path_y_list = []

    while (1):
        company = db.child("path").child(i).child("latitude").get()
        if (company.val() == None):
            break
        path_x_list.append(company.val())
        company_2 = db.child("path").child(i).child("longitude").get()
        path_y_list.append(company_2.val())
        i = i + 1

    guide = db.child("guide").get()
    point = db.child("pointIndex").get()

    x_list = list(map(float, path_x_list))
    y_list = list(map(float, path_y_list))
    direction_list = list(map(int, guide.val()))
    point_list = list(map(int, point.val()))


    guide_line = [1] * len(path_x_list)


    for i in range(0, len(point_list)):
        guide_line[point_list[i]] = direction_list[i]
        '''
        if guide_line[point_list[i]] == 2:
            left = str(point_list[i])
        elif guide_line[point_list[i]] == 3:
            right = str(point_list[i])
        '''

    return x_list, y_list, guide_line

def current_location():
    current_x = db.child("location").child("x").get()
    current_y = db.child("location").child("y").get()
    point_x = current_x.val()
    point_y = current_y.val()
    x = round(float(point_x), 5)
    y = round(float(point_y), 5)
    return x, y

def update_line(lidar, iterator, max_degree=360, min_degree=0, max_distance=600):
    angle = np.array([])
    distance = np.array([])
    left = 0
    right = 0

    offsets = np.array([(np.radians(angle), distance)])
    scan = next(iterator)
    for sn in range(len(scan)):
        if scan[sn][1] > min_degree and scan[sn][1] < max_degree:
            if scan[sn][2] < max_distance:
                # quality = np.append(quality, scan[sn][0])
                angle = np.append(angle, scan[sn][1])
                distance = np.append(distance, scan[sn][2])
                # rad=np.array([np.radians(scan[sn][1]), scan[sn][2]])
                left, right = div_demension(scan[sn][1], left, right)

    return angle, distance, left, right  # ,rad


def div_demension(angle, left, right):
    if angle >= 0 and angle < 90:
        # print('front_right')
        right += 1
    elif angle >= 90 and angle < 180:
        # print('front_left')
        left += 1
    elif angle >= 180 and angle < 270:
        print('back_left')

    else:
        print('back_right')

    return left, right


if __name__ == '__main__':
    # lidar = RPLidar(port='com3', baudrate=115200)

    x_list, y_list, guide_line = infomation()
    print(x_list)
    print(y_list)
    print(guide_line)

    #wheel = control.WheelHandler()
    left = 0
    right = 0
    offset = np.array([], [])

    index = 0
    #wheel.Forward()
    error_count = 0
    while True:
        angle_deg, distance, left, right = update_line(lidar=lidar, iterator=iterator, min_degree=0, max_degree=180, max_distance=200)
        offset = np.vstack([angle_deg, distance])

        x, y = current_location()

        if x - round(x_list[index], 5) <= abs(0.00003) and y - round(y_list[index], 5) <= abs(0.00003):  # 3m 이내에 접근한 경우
            if guide_line[index] == 2 or (left == 0 and right > 0):
                #wheel.ZC()
                #time.sleep(1.3)
                #wheel.FForward()
                print("Turn Left")
                index += 1
            elif guide_line[index] == 3 or (left > 0 and right == 0):
                #wheel.ZD()
                #time.sleep(1.3)
                #wheel.FForward()
                print("Turn Right")
                index += 1
            elif left > 0 and right > 0:
                #wheel.Stop()
                print("Stop")
            else:
                index += 1
                #wheel.FForward()
                print("Next Index")
                error_count = 0

        '''
        f = open('/home/pi/graduate_workspace/test/test.txt', 'w')
        left = str(left)
        right = str(right)
        f.write(right + '\n' + left + '\n')
        f.close()
        '''
        if index == len(guide_line):
            break
