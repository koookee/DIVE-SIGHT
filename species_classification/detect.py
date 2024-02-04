import tensorflow as tf
import os
import matplotlib.pyplot as plt
import cv2
import time

# Pre-trained model obtained from https://github.com/JeremyFJ/Shark-Detector
model = tf.saved_model.load('SL_modelv3')

DATADIR = './test_images/'

def analyze_image(image_np, threshold):
  input_tensor=tf.convert_to_tensor(image_np)
  input_tensor=input_tensor[tf.newaxis, ...]
  detections=model(input_tensor)
  num_detections=int(detections.pop('num_detections'))
  detections={key:value[0,:num_detections].numpy()
          for key,value in detections.items()}
  scores = detections['detection_scores']
  confidence = scores[0]
  
  print(f"Confidence score: {confidence}")
  return confidence

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