import tensorflow as tf
import os
import matplotlib.pyplot as plt
import cv2
import time
from image_capture import setup, take_picture, picam2

# Pre-trained model obtained from https://github.com/JeremyFJ/Shark-Detector
model = tf.saved_model.load('SL_modelv3')

DATADIR = './test_images/'
CAPTURED_IMAGES = './captured_images/'

def analyze_image(image_np, threshold):
  input_tensor=tf.convert_to_tensor(image_np)
  input_tensor=input_tensor[tf.newaxis, ...]
  detections=model(input_tensor)
  num_detections=int(detections.pop('num_detections'))
  detections={key:value[0,:num_detections].numpy()
          for key,value in detections.items()}
  scores = detections['detection_scores']
  confidence = scores[0]
  
  print(f"Confidence score that it's a shark: {confidence}")
  return confidence

def analyze_test_images():
    for img in os.listdir(DATADIR): # iterate through each image in DATADIR
        # time.sleep(3)
        img_name = img.split(".")[0]
        img = cv2.imread(DATADIR + img)
        threshold = 0.9 # threshold to determine whether image contains a shark or not -- adjust this based on sensitivity
        confidence = analyze_image(img, threshold)
        if confidence > threshold:
            print(f"{img_name} is a shark")
        else:
            print(f"{img_name} is not a shark")
        print("-----------------------------------------")
        plt.imshow(img)
        plt.show()

def analyze_captured_input():
    for i in range(0, 10):
        image_name = take_picture()
        img = cv2.imread(CAPTURED_IMAGES + image_name)
        threshold = 0.9 # threshold to determine whether image contains a shark or not -- adjust this based on sensitivity
        confidence = analyze_image(img, threshold)
        if confidence > threshold:
            print(f"{image_name} is a shark")
        else:
            print(f"{image_name} is not a shark")
        print("-----------------------------------------")
        time.sleep(5)

setup()
analyze_captured_input()