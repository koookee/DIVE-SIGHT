import tensorflow as tf
from tensorflow.keras import datasets, layers, models
import matplotlib.pyplot as plt
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

IMG_SIZE = 100

def convertToRGB(img_arr):
    return cv2.cvtColor(img_arr, cv2.COLOR_BGR2RGB)
    
def normalizeRGB(img_arr):
    return [[[color / 255.0 for color in column] for column in row] for row in img_arr]
    
def create_training_data():
    for category in CATEGORIES:

        path = os.path.join(DATADIR,category)  # create path
        class_num = CATEGORIES.index(category)  # get the classification 

        for img in tqdm(os.listdir(path)):  # iterate over each image 
            try:
                img_array = cv2.imread(os.path.join(path,img) ,cv2.IMREAD_GRAYSCALE)  # convert to array
                new_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))  # resize to normalize data size
                training_data.append([new_array, class_num])
            except Exception as e:
                pass
                print("OSErrroBad img most likely", e, os.path.join(path,img))
            except Exception as e:
                print("general exception", e, os.path.join(path,img))

def create_testing_data():
    for category in CATEGORIES:
        path = os.path.join(DATADIR,category+"Test")  # create path
        class_num = CATEGORIES.index(category)  # get the classification 

        for img in tqdm(os.listdir(path)):  # iterate over each image 
            try:
                img_array = cv2.imread(os.path.join(path,img) ,cv2.IMREAD_GRAYSCALE)
                new_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))
                testing_data.append([new_array, class_num])
            except Exception as e:
                pass
                print("OSErrroBad img most likely", e, os.path.join(path,img))
            except Exception as e:
                print("general exception", e, os.path.join(path,img))

def create_input_data():
    for category in CATEGORIES:
        path = os.path.join(DATADIR,category+"Input")  # create path
        class_num = CATEGORIES.index(category)  # get the classification 

        for img in tqdm(os.listdir(path)):  # iterate over each image 
            try:
                img_array = cv2.imread(os.path.join(path,img) ,cv2.IMREAD_GRAYSCALE)
                new_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))
                input_data.append([new_array, class_num])
            except Exception as e:
                pass
                print("OSErrroBad img most likely", e, os.path.join(path,img))
            except Exception as e:
                print("general exception", e, os.path.join(path,img))
                
create_training_data()
create_testing_data()
create_input_data()

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

IMG_INDEX = 150  # change this to look at other images

plt.imshow(train_images[IMG_INDEX] ,cmap=plt.cm.binary)
plt.xlabel(CATEGORIES[train_labels[IMG_INDEX]])
plt.show()

model = models.Sequential()
model.add(layers.Conv2D(64, (3, 3), activation='relu', input_shape=(100, 100, 1)))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))

model.add(layers.Flatten()) # We flatten because the convolutions are 2d and the dense layer is 1d
model.add(layers.Dense(64, activation='sigmoid'))
model.add(layers.Dense(2))

model.summary()

model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])

history = model.fit(train_images, train_labels, epochs=6,
                    validation_data=(test_images, test_labels), batch_size = 2)
                    
test_loss, test_acc = model.evaluate(test_images,  test_labels, verbose=2)
print(test_acc)

index = 7
plt.imshow(input_images[index] ,cmap=plt.cm.binary)
print(CATEGORIES[input_labels[index]])
plt.show()

predictions = model.predict(input_images)

for idx, pred in enumerate(predictions):
  plt.imshow(input_images[idx] ,cmap=plt.cm.binary)
  print(pred)
  print(f"Actual: {CATEGORIES[input_labels[idx]]}")
  print(f"Prediction: {CATEGORIES[pred.argmax()]}")
  plt.show()
  print("--------------------------------------------------------------------------")