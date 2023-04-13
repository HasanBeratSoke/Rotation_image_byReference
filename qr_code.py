import cv2
from pyzbar import pyzbar

image = cv2.imread('test2.png', cv2.IMREAD_GRAYSCALE)



barcodes = pyzbar.decode(image)

if(len(barcodes) == 0):

    print('qr code bulunamadı')

else:



    for barcode in barcodes:
        (x, y, w, h) = barcode.rect
        rect = barcode.rect
        center_x = int(x + w/2)
        center_y = int(y + h/2)
        center_qr = (int(rect.left + rect.width / 2), int(rect.top + rect.height / 2))
        #cv2.rectangle(image, (rect.left, rect.top), (rect.left + rect.width, rect.top + rect.height), (255, 0, 255), 2)
        #cv2.circle(image, center, 2, (255, 0, 255), 5)
        qr_code_text =  barcode.data.decode('utf-8')
        print(qr_code_text)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    cv2.imshow("QR Code Detection", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()