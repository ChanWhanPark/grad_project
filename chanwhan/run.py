import pyrebase
import time
#import control

start = time.time()
#wheel = control.WheelHandler()

## 정보 받아오기
config = {
    "apiKey" : "AIzaSyCWkh7qqUThfPx9XMAtWHwImaS_b4heJmA",
    "authDomain" : "chanwhan-37aa7.firebaseapp.com",
    "databaseURL" : "https://chanwhan-37aa7.firebaseio.com/",
    "storageBucket" : "chanwhan-37aa7.appspot.com"
}

firebase = pyrebase.initialize_app(config)

db = firebase.database()

f = open('test.txt', 'w')
left = 0
right = 0


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

    print("time :", time.time() - start)

    guide_line = [1] * len(path_x_list)

    print(len(guide_line))
    print(len(point_list))

    for i in range(0, len(point_list)):
        guide_line[point_list[i]] = direction_list[i]

    print(guide_line)
    print(type(guide_line))

    return x_list, y_list, guide_line


## 주행
if __name__ == '__main__':
    x_list, y_list, guide_line = infomation()
    index = 0
    error_count = 0
    #wheel.Forward()
    while (index != len(guide_line)):
        current_x = db.child("location").child("x").get()
        current_y = db.child("location").child("y").get()
        point_x = current_x.val()
        point_y = current_y.val()
        x = round(float(point_x), 5)
        y = round(float(point_y), 5)
        print("x: ", x)
        print("y: ", y)
        print("current index: ", index)
        print("current guide_line", guide_line[index])
        time.sleep(1)

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
        else: # 그렇지 않은 경우
            # Lidar Information
            if left == 0 and right > 0:
                print("Turn Left")
            elif left > 0 and right == 0:
                print("Turn Right")
            elif left == 0 and right == 0:
                print("Go Straight")
            else:
                print("Stop")

        error_count += 1

        if error_count == 100:
            #wheel.Backward()
            print("Go Back.")
            break
        if point_x == None:
            time.sleep(1)
            #wheel.Stop()
            print("No Direction.")
            break

    time.sleep(1)
    # wheel.Stop()
    if index == len(guide_line):
        print("Destination.")
    else:
        print("System Exit!!")

