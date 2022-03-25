from cgi import test
import numpy as np
import pandas as pd
import os
import cv2
import matplotlib.pyplot as plt


train_path="/Users/dbarblishvili/go/src/grpc-go-course/Part_Identifier/part_identifier_server/part_recognition/data/train_data"
test_path="/Users/dbarblishvili/go/src/grpc-go-course/Part_Identifier/part_identifier_server/part_recognition/data/test_data"


x_train=[]

for img in os.listdir(train_path):
    if not img.endswith('.png'):
        continue
    image_path=train_path+"/"+img
    img_arr=cv2.imread(image_path)
    img_arr=cv2.resize(img_arr,(224,224))
    x_train.append(img_arr)



x_test=[]

for img in os.listdir(test_path):
    if not img.endswith('.png'):
        continue
    image_path=test_path+"/"+img
    img_arr=cv2.imread(image_path)
    img_arr=cv2.resize(img_arr,(224,224))
    x_test.append(img_arr)


