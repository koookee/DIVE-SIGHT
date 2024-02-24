import tensorflow as tf
import os
import matplotlib.pyplot as plt
import cv2
import time
import sys

if not 'model_evaluation':
    from image_capture import setup, take_picture, picam2

# Pre-trained model obtained from https://github.com/JeremyFJ/Shark-Detector
model = tf.saved_model.load('SL_modelv3')

SHARK_IMG_DIR = './test_images/shark_images/' # For model evaluation
NONSHARK_IMG_DIR = './test_images/nonshark_images/' # For model evaluation

CAPTURED_IMAGES = './captured_images/' # Captured images from the Raspberry Pi camera

threshold = 0.9 # threshold to determine whether image contains a shark or not -- adjust this based on sensitivity

eval_threshold = 0 # For evaluating the model with different threshold values

true_positives, false_negatives, false_positives, true_negatives = 0, 0, 0, 0

def analyze_image(image_np, threshold):
  input_tensor=tf.convert_to_tensor(image_np)
  input_tensor=input_tensor[tf.newaxis, ...]
  detections=model(input_tensor)
  num_detections=int(detections.pop('num_detections'))
  detections={key:value[0,:num_detections].numpy()
          for key,value in detections.items()}
  scores = detections['detection_scores']
  confidence = scores[0]
  
  if 'trace' in sys.argv: 
    print(f"Confidence score that it's a shark: {confidence}")
  return confidence

def analyze_test_images(IMG_DIR, is_shark):
    global true_positives, false_negatives, false_positives, true_negatives
    for img in os.listdir(IMG_DIR): # iterate through each image in the image directory
        img_name = img.split(".")[0]
        img = cv2.imread(IMG_DIR + img)
        confidence = analyze_image(img, eval_threshold)
        predicted_shark = confidence > eval_threshold # True if the model predicted that the image contains a shark; false otherwise
        if (predicted_shark) and is_shark:
            true_positives += 1
        elif (not predicted_shark) and is_shark:
            false_negatives += 1
        elif (predicted_shark) and not is_shark:
            false_positives += 1
        elif (not predicted_shark) and not is_shark:
            true_negatives += 1
        

def analyze_captured_input():
    for i in range(0, 10):
        image_name = take_picture()
        img = cv2.imread(CAPTURED_IMAGES + image_name)
        confidence = analyze_image(img, threshold)
        if confidence > threshold:
            print(f"{image_name} is a shark")
        else:
            print(f"{image_name} is not a shark")
        print("-----------------------------------------")
        time.sleep(5)

def plot_roc():
    global eval_threshold, true_positives, false_negatives, false_positives, true_negatives
    threshold_lst = [x/10 for x in range(0, 11)]
    for i in threshold_lst:
        true_positives, false_negatives, false_positives, true_negatives = 0, 0, 0, 0
        eval_threshold = i
        analyze_test_images(SHARK_IMG_DIR, True)
        analyze_test_images(NONSHARK_IMG_DIR, False)
        print(f"TP: {true_positives}      |     FN: {false_negatives}")
        print(f"FP: {false_positives}      |     TN: {true_negatives}")
        print(f"Threshold: {eval_threshold}")
        print("--------------------------------------------------------------")

if 'model_evaluation' in sys.argv: 
    plot_roc()
else:
    setup()
    analyze_captured_input()