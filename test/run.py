import pyrebase
import time
import control

start = time.time()
wheel = control.WheelHandler()

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

i = 0
path_x_list = []
path_y_list = []

while(1):
    company = db.child("path").child(i).child("latitude").get()
    if (company.val() == None):
        break
    path_x_list.append(company.val())
    company_2 = db.child("path").child(i).child("longitude").get()
    path_y_list.append(company_2.val())
    print(company.val())
    print(company_2.val())
    i = i + 1


company_3 = db.child("guide").get()
company_4 = db.child("pointIndex").get()
print(path_x_list)
print(path_y_list)
print(company_3.val())
print(company_4.val())
print(type(company_3.val()))

x_list = list(map(float, path_x_list))
y_list = list(map(float, path_y_list))
direction_list = list(map(int, company_3.val()))
point_list = list(map(int, company_4.val()))

print("time :", time.time() - start)

guide_line = [1] * len(path_x_list)

print(len(guide_line))
print(len(point_list))

for i in range(0, len(point_list)):
    guide_line[point_list[i]] = direction_list[i]
    if guide_line[point_list[i]] == 2:
        left = str(point_list[i])
        f.write("left: " + left + '\n')
        print("left 입력")
    elif guide_line[point_list[i]] == 3:
        right = str(point_list[i])
        f.write("right: " + right + '\n')
        print("right 입력")

print(guide_line)
print(type(guide_line))
f.close()

## 주행
index = 0
error_count = 0
rotate_count = 0
straight_count = 0
wheel.Forward()
while (index != len(guide_line)):
    current_x = db.child("location").child("x").get()
    current_y = db.child("location").child("y").get()
    point_x = current_x.val()
    point_y = current_y.val()
    x = round(float(point_x), 5)
    y = round(float(point_y), 5)
    print("x: " ,x)
    print("y: ", y)
    print("current index: ", index)
    print("current guide_line", guide_line[index])
    time.sleep(3)
    error_count += 1
    if x - round(x_list[index], 5) <= abs(0.00003) and y - round(y_list[index], 5) <= abs(0.00003): # 3m 이내에 접근한 경우
        index += 1

        if guide_line[index] == 2 or guide_line[index] == 3:
            if guide_line[index] == 2:
                wheel.ZC()
                time.sleep(1.3)
                wheel.FForward()
                print("Turn Left")

            elif guide_line[index] == 3:
                wheel.ZD()
                time.sleep(1.3)
                wheel.FForward()
                print("Turn Right")

        else:
            index += 1
            wheel.FForward()
            error_count = 0

    if error_count == 100:
        wheel.Backward()
        print("Go Back.")
        break
    if point_x == None:
        time.sleep(1)
        wheel.Stop()
        print("No Direction.")
        break

if guide_line[index-1] == 88:
    time.sleep(1)
    wheel.Stop()
    print("Destination.")
print("System Exit!!")
