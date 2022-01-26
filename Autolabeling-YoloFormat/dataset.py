import cv2
import os


cam = cv2.VideoCapture(0)
cam.set(3, 640) # set video width
cam.set(4, 480) # set video height

w_img = 640
h_img = 480

#make sure 'haarcascade_frontalface_default.xml' is in the same folder as this code
face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

db = open("dataset/labels.names", "r")
face_id = 0
for line in db:
    face_id += 1

# For each person, enter one numeric face id (must enter number start from 1, this is the lable of person 1)
# face_id = input('\n enter user id and press <return> ==>  ')
name = input('\n enter name and press <return> ==>  ')

print("\n [INFO] Initializing face capture. Look the camera and wait ...")
# Initialize individual sampling face count
count = 0

#start detect your face and take 30 pictures
while(True):

    ret, img = cam.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(gray, 1.3, 5)

    for (x,y,w,h) in faces:

        cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)     
        count += 1
        # Save the captured image into the datasets folder
        cv2.imwrite("dataset/User." + str(face_id) + '.' + str(count) + ".jpg", gray)

        # Save label 
        f = open("dataset/User." +  str(face_id) + '.' + str(count) + ".txt" , "a")
        f.write("%s %f %f %f %f" % ( face_id, (x+w/2)/w_img, (y+h/2)/h_img, w/w_img, h/h_img ))
        print("%s %f %f %f %f" % ( face_id, (x+w/2)/w_img, (y+h/2)/h_img, w/w_img, h/h_img ))
        f.close()

        cv2.imshow('image', img)

    k = cv2.waitKey(100) & 0xff # Press 'ESC' for exiting video
    if k == 27:
        break
    elif count >= 30: # Take 30 face sample and stop video
         break

f = open("dataset/labels.names", "a")
f.write(name + "\n")
f.close()


# Do a bit of cleanup
print("\n [INFO] Exiting Program and cleanup stuff")
cam.release()
cv2.destroyAllWindows()


