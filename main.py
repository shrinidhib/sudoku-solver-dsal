import cv2
import numpy as np
from utilities import * 
from keras.models import load_model
import keras
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras import backend as K
import easyocr
from paddleocr import PaddleOCR
import solver
import os
from backend import filename
from PIL import Image
import PIL



height=450
width=450

#preprocess
img=cv2.imread('sudoku.png')
final=cv2.imread('static/Images/empty_sud.png')
final=cv2.resize(final,(width,height))
img=cv2.resize(img,(width,height))
imgBlank=np.zeros((height,width,3),np.uint8)
imgThresh=preprocess(img)

#find contours outer box only
imgcontour=img.copy()
imgbigcontour=img.copy()
contours,hierarchy=cv2.findContours(imgThresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
cv2.drawContours(imgcontour,contours,-1,(0,255,0),3)

#biggest contour
biggest,maxarea=biggestcontour(contours)

if biggest.size!=0:
    biggest=reorder(biggest)
    cv2.drawContours(imgbigcontour,biggest,-1,(0,255,0),10)
    pts1=np.float32(biggest)
    pts2=np.float32([[0,0],[width,0],[0,height],[width,height]])
    matrix=cv2.getPerspectiveTransform(pts1,pts2)
    warpcolor=cv2.warpPerspective(img,matrix,(width,height))
    Detecteddigitss=imgBlank.copy()
    warpcolor=cv2.cvtColor(warpcolor,cv2.COLOR_BGR2GRAY)


#find each box
boxes=splitboxes(warpcolor)
#getprediction(boxes)

reader=easyocr.Reader(['en'])
ocr_model = PaddleOCR(use_angle_cls=True,lang='en', use_gpu=True)

sudoku_board=[]

for i in range(len(boxes)):
    result = ocr_model.ocr(boxes[i])
    if len(result)!=0:
        for idx in range(len(result)):
            res = result[idx]
            print(res[1][0])
            sudoku_board.append(int(res[1][0]))
    else:
        sudoku_board.append(0)

print(sudoku_board)
sudoku=[]
for i in range(9):
    sudoku.append(sudoku_board[i*9:i*9+9])

for i in sudoku:
    print(i)

print("\n\n")
solver.solver(sudoku)
for i in sudoku:
    print(i)
s=imgBlank.copy()
sud=[]
for i in sudoku:
    for j in i:
        sud.append(j)
s=display(final,sudoku_board,sud)
cv2.imwrite('static/Images/final.png', s)
