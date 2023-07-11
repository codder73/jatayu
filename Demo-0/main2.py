import face_recognition
import  os
import cv2
import numpy as np
from collections import Counter
from time import sleep
import time
import csv
from datetime import datetime
from dataset import dic_name

images = []
className = []
cnting = []
time_limit = 15

path = 'Images/'
mylist = os.listdir(path)

for cl in mylist:
    curImg = cv2.imread(f"{path}/{cl}")
    images.append(curImg)
    className.append(os.path.splitext(cl)[0])#removing extensions 

def get_most_frequent_value(lst):
    counter = Counter(lst)
    most_common = counter.most_common(1)
    return most_common[0][0]# if most_common else None

total_students = len(className)
present_name = className.copy()


def styleCsv():
    frst_str = f'**Welcome, This is Core grops Attedance**\nTotal number of students are - {total_students}\n\nName, School Num, Time'
    num_list = []
    now = datetime.now()
    fdate = now.strftime("%Y,%m,%d ")
    with open(f"{fdate}.csv", 'a+') as f:
            with open(f'{fdate}.csv', 'rt') as j:
                reader = csv.reader(j, delimiter=',') # good point by @paco
                for row in reader:
                    for field in row:
                        if 'Welcome' in field:
                            num_list.append(1)
                        else:
                            num_list.append(0)
            if 1 not in num_list:
                f.writelines(frst_str)
            elif 1 in num_list:
                pass
            print(num_list)
    

def markAttendance2(nam, sch_num):
    now = datetime.now()
    fdate = now.strftime("%Y,%m,%d ")
    present_list = []
    ftime = now.strftime("%H:%M:%S")
    username = nam
    with open(f"{fdate}.csv", 'a+') as f:
        # f.writelines("Name, Sch_num, Time")    
        myDataList = f.readlines()
        with open(f'{fdate}.csv', 'rt') as j:
            reader = csv.reader(j, delimiter=',') # good point by @paco
            for row in reader:
                for field in row:
                    if field == username:
                        is_in_file = 1
                        present_list.append(is_in_file)
                    else:
                        is_in_file = 0
                        present_list.append(is_in_file)
        if 1 not in present_list:
            f.writelines(f"\n{nam}, {sch_num}, {ftime}")
        elif 1 in present_list:
            print("You are already marked present")

    
def findEncodings(images):
    encodelist = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodelist.append(encode)
    return encodelist

encodelistKnown = findEncodings(images)

def main_func():
    cap = cv2.VideoCapture(0)

    for p in range(6):
        while True:
            success, img = cap.read()
            imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
            imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

            facesCurFrame = face_recognition.face_locations(imgS)

            if len(facesCurFrame) == 1:#means if any face is present...
                encodesCurFrame = face_recognition.face_encodings(imgS,facesCurFrame)#first finding encodings of it

                for encodeFace, Faceloc in zip(encodesCurFrame, facesCurFrame):#now turn by turn access them 
                        matches = face_recognition.compare_faces(encodelistKnown, encodeFace)#and match them
                        faceDis = face_recognition.face_distance(encodelistKnown, encodeFace)#and find face distance

                        if True in matches:
                            matchIndex = np.argmin(faceDis)
                            if matches[matchIndex]:
                                name = className[matchIndex]
                                name1 = str(name)
                                ser_num = int(name)
                                cnting.append(ser_num)                                
                                # present_index = className.index(name1)
                                # className.remove(present_index)
                                # del className[present_index]
                        else:
                            cnting.append(0)
                            # print("Unknown Face")
            else:
                continue
            break
        

if __name__=='__main__':
    start_time = time.time()
    styleCsv()
    while 1:
        main_func()

        print(cnting)
        print("length of cnting",len(cnting))
        
        if len(cnting) != 6:
            main_func()
        elif len(cnting) == 6:
            max_num = get_most_frequent_value(cnting)
            print(max_num)
            if max_num == 0:
                print("unknown face")
            elif max_num != 0:
                nam_sch = dic_name(max_num)
                print("Name is: ", nam_sch[1])#name
                print("Schl num is : ", nam_sch[0])#sch num
                
                markAttendance2(nam_sch[1], nam_sch[0])

        cnting.clear()
        str_max = str(max_num)
        # className.remove(max_num)
        # present_index = className.index(str_max)
        print("present num : ",str_max)
        if str_max == '0':
            print("Your face didn't matched with the existing database...")
        elif str_max != '0':
            try:
                present_name.remove(str_max)
            except:
                print("You are already marked present!") 

        for i in range(4):
            print(i)
            sleep(1)

        print('class list- ',className)
        print('class list copy- ', present_name)

        elapsed_time = time.time() - start_time
        if elapsed_time >= time_limit:
            break
    
    now = datetime.now()
    fdate = now.strftime("%Y,%m,%d ")
    prsnt_students = len(className) - len(present_name)
    # print(len(present_name))
    with open(f"{fdate}.csv", 'a+') as f:
        f.writelines(f'\nThe number of students present are: {prsnt_students}')
        f.writelines(f'\n\nThe number of students absent: {len(present_name)},\nAbsent Students: ')
        print(f'The number of students absent: {len(present_name)},\nAbsent Students: ')
        for num2  in present_name:
            num2 = int(num2)
            # from dataset import dic_name
            nam_sch2 = dic_name(num2)
            name2 = nam_sch2[1]
            sch_num2 = nam_sch2[0]
            print("Name is: ", name2)#name
            print("School num is : ", sch_num2)#sch num

            f.writelines(f'{name2},{sch_num2}')
    

    # break

# print(className)
# markAttendance2(splt[1], splt[2])

        # if len(facesCurFrame) == 1: