import cv2
import numpy as np
import json
import os
import requests

url = 'http://192.168.26.12/data' 

cap = cv2.VideoCapture("https://192.168.26.114:8080/video") # Open the default camera
while True:

    ret, frame = cap.read() # Read a frame from the video stream
    if not ret:
        continue
    
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        print(data['potentiometer'])
        if data['potentiometer'] >= 2.0:
            
            cv2.imwrite('./images/red_laser_spot.jpg', frame)
        
    cv2.imshow('frame', frame) # Display the frame
    if cv2.waitKey(1) == ord('q'): # Quit on 'q' key
        break

    file_path = "./images/red_laser_spot.jpg"
    if os.path.exists(file_path):
        img = cv2.imread("./images/red_laser_spot.jpg")
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (3, 3), 0)
        minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(blur)

        image = cv2.circle(img, maxLoc, 30, (0, 255, 0), 2)
        cv2.imwrite("./video/image.jpg", image)

        with open("./coordinate/coor.txt", "w") as f:
            f.write(str(maxLoc[0])+","+"\t")
            f.write(str(1080-maxLoc[1]))
    else:
        print("file is not exist")

cap.release() # Release the video stream
cv2.destroyAllWindows() # Destroy all windows