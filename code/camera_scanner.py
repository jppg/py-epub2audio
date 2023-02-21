import os
import cv2
from datetime import datetime

HOME_PATH = "output"

if not os.path.isdir(HOME_PATH):
    os.makedirs(HOME_PATH)

url = 'http://10.10.0.206:8080/video'
cap = cv2.VideoCapture(url)
while(True):
    ret, frame = cap.read()
    if frame is not None:
        cv2.imshow('frame',frame)
    
    # Press Space to take a snapshot
    if cv2.waitKey(1) == 32:
        exec_date = datetime.now()
        exec_date_str = exec_date.strftime("%Y-%m-%d-%H%M%S")

        img_path = os.path.join(HOME_PATH,exec_date_str +".png")
        cv2.imwrite(img_path, frame)

    # Press Esc key to exit
    if cv2.waitKey(1) == 27:
        break

cv2.destroyAllWindows()