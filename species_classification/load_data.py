import numpy as np
import os
import cv2
from tqdm import tqdm
import random

DATADIR = "datasets"

CATEGORIES = ["hammerhead", "mako"]

training_data = []
testing_data = []
input_data = []

IMG_SIZE = 150

def convertToRGB(img_arr):
    return cv2.cvtColor(img_arr, cv2.COLOR_BGR2RGB)
    
def normalizeRGB(img_arr):
    return [[[color / 255.0 for color in column] for column in row] for row in img_arr]
    
def create_data_arr(data_arr, data_type):
    for category in CATEGORIES:

        path = os.path.join(DATADIR,category+data_type)  # create path
        class_num = CATEGORIES.index(category)  # get the classification 

        for img in tqdm(os.listdir(path)):  # iterate over each image 
            try:
                img_array = cv2.imread(os.path.join(path,img) ,cv2.IMREAD_GRAYSCALE)  # convert to array
                new_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))  # resize to normalize data size
                data_arr.append([new_array, class_num])
            except Exception as e:
                pass
                print("OSErrroBad img most likely", e, os.path.join(path,img))
            except Exception as e:
                print("general exception", e, os.path.join(path,img))

create_data_arr(training_data, "Training")
create_data_arr(testing_data, "Test")
create_data_arr(input_data, "Input")

random.shuffle(training_data)
random.shuffle(testing_data)
random.shuffle(input_data)

print(len(training_data))
# print(training_data)

train_images = []
train_labels = []

test_images = []
test_labels = []

input_images = []
input_labels = []

for features,label in training_data: 
    train_images.append(features)
    train_labels.append(label)

for features,label in testing_data: 
    test_images.append(features)
    test_labels.append(label)

for features,label in input_data: 
    input_images.append(features)
    input_labels.append(label)

print(train_images[0].reshape(-1, IMG_SIZE, IMG_SIZE, 1))

train_images = np.array(train_images).reshape(-1, IMG_SIZE, IMG_SIZE, 1)
train_labels = np.array(train_labels)

test_images = np.array(test_images).reshape(-1, IMG_SIZE, IMG_SIZE, 1)
test_labels = np.array(test_labels)

input_images = np.array(input_images).reshape(-1, IMG_SIZE, IMG_SIZE, 1)
input_labels = np.array(input_labels)

train_images = train_images/255.0
test_images = test_images/255.0
input_images = input_images/255.0