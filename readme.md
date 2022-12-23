# Rotation image by two reference point

### Method
1. Convert image to HSV plate and apply yellow mask.
   ```python
    #convert HSV plate
    f_hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    
    #add litle bit blur
    img_gausblur = cv.GaussianBlur(f_hsv, (3, 3), 0)
    
    # yellow hsv color range
    lower_blue = np.array([28, 255, 255])
    upper_blue = np.array([30, 255, 255])
    
    # treshhold on yellow
    yellow_mask = cv.inRange(img_gausblur, lower_blue, upper_blue)

   ```
2. Find center of the image and draw circle.
   ```python
    center = (round(w / 2), round(h / 2))
    center_top = (round((w/2)+1), round(h/7))
    f_dots = cv.circle(yellow_mask, center, 5, (255,255,0), -1)
   ```
3. Find coordinate and assign the values.
   1. coordinate of the reference point.
   ```python
   contours, _ = cv.findContours(yellow_mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
   contours = sorted(contours, key=lambda x: cv.contourArea(x), reverse=True)
    for i in contours:
        M = cv.moments(i)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        (x, y, w, h) = cv.boundingRect(i)
        c_ref = (cX, cY)
        break
   ```
   2. coordinate of the center of image.
   3. coordinate of the where you want to rotation.
4. Find slop of the line that from center to reference point.
   ```python
    x1 = center[0]
    y1 = center[1]
    x3 = cX
    y3 = cY

    m2 = float((y3-y1) / (x3 - x1))
    print('slope m2: ', m2)
   ```
1. Convert slope to degree.
    ```python
    xtan = math.atan(m2) #radyan sonucu
    m2_deg = math.degrees(xtan)  # dereye cevrildi
    ```
3. Split image four area and detect which area the point and Rotate image by degree.
   ```python
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
   ```


<p align="center">
  <img src="https://github.com/HasanBeratSoke/leaves-segmentation/  blob/main/rgbd_plant.gif" />
</p>