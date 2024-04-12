import cv2
import numpy as np
import pytesseract
from keras.models import load_model

def preprocess(img):
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    blur=cv2.GaussianBlur(gray,(5,5),1)
    imgThresh=cv2.adaptiveThreshold(blur,255,1,1,11,2)
    return imgThresh

def biggestcontour(contour):
    biggest=np.array([])
    max_area=0
    for i in contour:
        area=cv2.contourArea(i)
        if area>50:
            peri=cv2.arcLength(i,True)
            approx=cv2.approxPolyDP(i,0.02*peri,True)
            if area>max_area and len(approx)==4:
                biggest=approx
                max_area=area
    return biggest,max_area

def reorder(points):
    points=points.reshape((4,2))
    p=np.zeros((4,1,2),dtype=np.int32)
    add=points.sum(1)
    p[0]=points[np.argmin(add)]
    p[3]=points[np.argmax(add)]
    diff=np.diff(points,axis=1)
    p[1]=points[np.argmin(diff)]
    p[2]=points[np.argmax(diff)]
    return p

def splitboxes(warped):
    rows=np.vsplit(warped,9)
    boxes=[]
    for i in rows:
        cols=np.hsplit(i,9)
        for box in cols:
            boxes.append(box)
    return boxes

def getprediction(boxes):
    for i in range(len(boxes)):
        print(predict(boxes[i]))


def predict(img):
    image = img.copy()
    # image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # image = cv2.threshold(image, 140, 255, cv2.THRESH_BINARY)[1]
    image = cv2.resize(image, (28, 28))
    # display_image(image)
    image = image.astype('float32')
    image = image.reshape(1, 28, 28, 1)
    image /= 255

    # plt.imshow(image.reshape(28, 28), cmap='Greys')
    # plt.show()
    model = load_model('model.h5')
    pred = model.predict(image.reshape(1, 28, 28, 1), batch_size=1)
    return pred.argmax()


def display(img,nums_initial,nums,color=(0,255,)):
    secW=int(img.shape[1]/9)
    secH=int(img.shape[0]/9)
    for x in range(9):
        for y in range(9):
            
            if nums_initial[(y*9)+x]!=0:
                cv2.putText(img,str(nums_initial[(y*9)+x]),(x*secW+int(secW/2)-10,int((y+0.8)*secH)),cv2.FONT_HERSHEY_COMPLEX,1.5,(63, 13, 181),3,cv2.LINE_AA)
            else:
                cv2.putText(img,str(nums[(y*9)+x]),(x*secW+int(secW/2)-10,int((y+0.8)*secH)),cv2.FONT_HERSHEY_COMPLEX,1.5,(0,0,0),2,cv2.LINE_AA)
    return img