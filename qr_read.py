import cv2
import sys
from pyzbar.pyzbar import decode
import numpy as np

def qr_read():
    delay = 1
    window_name = 'frame'

    cap = cv2.VideoCapture('/dev/v4l/by-id/usb-9726-200619_Integrated_Camera-video-index0')

    if not cap.isOpened():
        sys.exit()

    while True:
        ret, frame = cap.read()
        k = False
        #cv2.imshow(window_name, frame)
        if ret:
            for d in decode(frame):
                s = d.data.decode()
                k = get_coords(s)
                frame = cv2.rectangle(frame, (d.rect.left, d.rect.top),
                                    (d.rect.left + d.rect.width, d.rect.top + d.rect.height), (0, 255, 0), 3)
                frame = cv2.putText(frame, s, (d.rect.left, d.rect.top + d.rect.height),
                                    cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 2, cv2.LINE_AA)
            cv2.imshow(window_name, frame)
        if (cv2.waitKey(delay) & 0xFF == ord('q')) or k:
            break

    cv2.destroyWindow(window_name)

def get_coords(s):
    coords1 = []
    coords2 = []
    if(s!=''):
        x = s.split(",")
        if(np.size(x)==4):
            coords1.append(float(s.split(",")[0][2:]))
            coords1.append(float(s.split(",")[1][:-1]))
            coords2.append(float(s.split(",")[2][1:]))
            coords2.append(float(s.split(",")[3][:-2]))
            coords = np.array([coords1, coords2])
        elif(np.size(x)==2):
            coords1.append(float(s.split(",")[0][1:]))
            coords1.append(float(s.split(",")[1][:-1]))
            coords = np.array(coords1)
        print(coords)
        return True
    else:
        return False

qr_read()