import math

from pynput.mouse import Button, Controller
import numpy as np
import mediapipe as mp
import math
import cv2 as cv
import face_and_hand_module
mouse = Controller()
hand=face_and_hand_module.Hand(False,1,0.7,0.7)
cap=cv.VideoCapture(1)
cap.set(cv.CAP_PROP_FRAME_HEIGHT,600)
cap.set(cv.CAP_PROP_FRAME_WIDTH,800)
cap.set(cv.CAP_PROP_FPS,60)
xp=0
yp=0
smoothing=7
ptime=0
plocx,plocy=0,0
clocx,clocy=0,0
while cap.isOpened():

    _,image=cap.read()
    cv.flip(image,1,image)
    image=hand.find_hands(image)
    List=hand.findPost(image,0)
    finger_tip=[4,8,12,16,20]
    upper_finger=hand.finner_up_count(List)
    x_mouse=0
    y_mouse=0

    if len(List)!=0:

        #create a rectange region and do something only if index finger is inside the rectange
        Mouse_Screen_x=image.shape[1]-100
        Mouse_Screen_y = image.shape[0] - 170
        cv.rectangle(image,(100,30),(Mouse_Screen_x,Mouse_Screen_y),(0,255,0),1)

        if (List[8][1]>100 and List[8][1]<Mouse_Screen_x)&(List[8][2]>30 and List[8][2]<Mouse_Screen_y):

           if upper_finger.count(1)>2 or upper_finger.count(0)==5:
               pass

           elif upper_finger[1]==1 and upper_finger[2]==1:
               x1, y1 = List[finger_tip[1]][1:]
               x2, y2 = List[finger_tip[2]][1:]
               x = (x1 + x2) // 2
               y = (y1 + y2) // 2
               cv.line(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
               length=int(math.hypot(x1-x2,y1-y2))
               print(length)
               if length>20:
                   cv.circle(image, (x, y), 10, (255, 0, 255), cv.FILLED)

               else:
                   cv.circle(image, (x, y), 10, (0, 255, 255), cv.FILLED)
                   mouse.press(Button.left)
                   mouse.release(Button.left)
                   cv.waitKey(120)






           else:
               cv.circle(image, List[8][1:], 10, (0, 0, 255), cv.FILLED)

               x_mouse=int(np.interp(List[8][1],[110,Mouse_Screen_x],[0,4000]))#change it to 1700x950
               y_mouse=int(np.interp(List[8][2],[40,Mouse_Screen_y],[0,2300]))

               #smmoting
               clocx=plocx+(x_mouse-plocx)/smoothing
               clocy=plocy+(y_mouse-plocy)/smoothing



               mouse.position=(clocx,clocy)
               print(mouse.position)
               plocx,plocy=clocx,clocy





        #index finger up

         #draw a cricle on finder index


         #normalize it to the screen size





    cv.imshow("pointer",image)

    if cv.waitKey(1)& 0xFF==27:
        break;

