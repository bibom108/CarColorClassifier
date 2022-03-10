import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.cluster import KMeans
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from collections import Counter
import torch

model = tf.keras.models.load_model('colormodel_trained_90.h5')
draw = False
cor = []
color_dict={
    0 : 'Red',
    1 : 'Green',
    2 : 'Blue',
    3 : 'Yellow',
    4 : 'Orange',
    5 : 'Pink',
    6 : 'Purple',
    7 : 'Brown',
    8 : 'Grey',
    9 : 'Black',
    10 : 'White'
}

def catch_point(event, x, y, flags, param):
    global draw, cur_x, cur_y, cor, tmp_img, draw_img
    if event == cv.EVENT_LBUTTONDOWN:
        draw = True
        cur_x = x
        cur_y = y
    elif event == cv.EVENT_MOUSEMOVE:
        if draw == True:
            tmp_img = draw_img.copy()
            cv.rectangle(tmp_img, (cur_x, cur_y), (x, y), (36,255,12), 2)
            cv.imshow("draw_img", tmp_img)
    elif event == cv.EVENT_LBUTTONUP:
        draw_img = cv.rectangle(draw_img, (cur_x, cur_y), (x, y), (36,255,12), 2)
        cor.append([cur_x, cur_y, x, y])
        draw = False


def drawBox(x1, y1, x2, y2, text, img):
    img = cv.rectangle(img, (x1, y1), (x2, y2), (36,255,12), 2)
    img = cv.putText(img, text, (x1, y1-5), cv.FONT_HERSHEY_SIMPLEX, 0.5, (36,255,12), 2, cv.LINE_AA)


def predict_color(Red, Green, Blue):
    rgb = np.asarray((Red, Green, Blue)) #rgb tuple to numpy array
    input_rgb = np.reshape(rgb, (-1,3)) #reshaping as per input to ANN model
    color_class_confidence = model.predict(input_rgb) # Output of layer is in terms of Confidence of the 11 classes
    color_index = np.argmax(color_class_confidence, axis=1) #finding the color_class index from confidence
    color = color_dict[int(color_index)]
    return color


def getColor(cur):
    cur = cur.reshape((cur.shape[0] * cur.shape[1], 3))
    clt = KMeans(10)
    labels = clt.fit_predict(cur)
    label_counts = Counter(labels)
    dominant_color = clt.cluster_centers_[label_counts.most_common(1)[0][0]]
    return predict_color(dominant_color[2], dominant_color[1], dominant_color[0])


def resetFunc():
    global cor
    cor = []


def mainFunc(img_path):
    # FILE
    img = cv.imread(img_path)

    # GET COR BY YOLOV5
    model_yolov = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
    results = model_yolov(img)
    results = results.pandas().xyxy[0].to_numpy()
    for x in results:
        if x[6] == 'car':
            cor.append([int(x[0]), int(x[1]), int(x[2]), int(x[3])])

    # GET COLOR
    for x in cor:
        tmp = img[x[1]:x[3], x[0]:x[2]]
        text = getColor(tmp)
        drawBox(x[0], x[1], x[2], x[3], text, img)
    return img