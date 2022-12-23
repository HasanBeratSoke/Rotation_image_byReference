import cv2 as cv
import math
import numpy as np
from skimage.transform import (hough_line, hough_line_peaks)
from PIL import Image
import sys

IMG_PATH = 'test7.png'
frame = cv.imread(IMG_PATH)
im = Image.open(IMG_PATH)
cv.imshow('frame', frame)

#convert HSV plate
f_hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

#add litle bit blur
img_gausblur = cv.GaussianBlur(f_hsv, (3, 3), 0)

# yellow hsv color range
lower_blue = np.array([28, 255, 255])
upper_blue = np.array([30, 255, 255])

# treshhold on yellow
yellow_mask = cv.inRange(img_gausblur, lower_blue, upper_blue)

#find coordinate point



contours, _ = cv.findContours(yellow_mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
if len(contours) == 0:
    # eğer referasn noktası yoksa orginal resmi döndürecek
    #sys.exit()
    print('referans noktaları tespit edilemedi.')
    quit()

else:
    contours = sorted(contours, key=lambda x: cv.contourArea(x), reverse=True)
    for i in contours:
        M = cv.moments(i)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        (x, y, w, h) = cv.boundingRect(i)
        c_ref = (cX, cY)
        break


# draw circle center of the image
(h, w) = frame.shape[:2]
rows, cols, _ = frame.shape
print((h,w),rows, cols)
center = (round(w / 2), round(h / 2))
center_top = (round((w/2)+1), round(h/7))

f_dots = cv.circle(yellow_mask, center, 5, (255,255,0), -1)

# draw line
f_dots = cv.line(f_dots, center_top, center,(255,255,0),2,lineType=8)
f_dots = cv.line(f_dots, center, c_ref,(255,255,0),2,lineType=8)
cv.imshow('line', f_dots)


# FIND ANGLE BETWEEN TWO LINES

#eğim
#döndürmek istediğimiz düzlemin eğimi
x1 = center[0]
y1 = center[1]
x2 = center_top[0]
y2 = center_top[1]
x3 = cX
y3 = cY

m2 = float((y3-y1) / (x3 - x1))
print('slope m2: ', m2)
xtan = math.atan(m2) #radyan sonucu
m2_deg = math.degrees(xtan)  # dereye cevrildi
print('m2_deg: ',m2_deg)


def rotation_image(angle):
    # Görüntü matrisini bir açı derecesinde döndür
    matris = cv.getRotationMatrix2D((w/2, h/2), angle, 1)
    döndürülmüş_resim = cv.warpAffine(frame, matris, (w, h))
    cv.imshow('rotated_image', döndürülmüş_resim) 

# Noktanın koordinatları
x = cX
y = cY
# Noktanın hangi bölgede olduğunu bul
if x <w / 2 and y < h / 2:
    # Görüntü matrisini bir açı derecesinde döndür
    print("Sol üst köşe")
    angle = round(270 + m2_deg)
    rotation_image(angle)
elif x < w / 2 and y >= h / 2:
    print("Sol alt köşe")
    angle = round(180 + (90 + m2_deg))
    rotation_image(angle) 
elif x >= w / 2 and y < h / 2:
    print("Sağ üst köşe")
    angle = round(90 + m2_deg  )
    rotation_image(angle)
else:
    print("Sağ alt köşe")
    angle = round(90 + m2_deg  )
    rotation_image(angle)


cv.waitKey(0)
cv.destroyAllWindows()