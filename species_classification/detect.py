import tensorflow as tf
import os
import numpy as np
from scipy.interpolate import make_interp_spline
import matplotlib.pyplot as plt
import cv2
import time
import sys

if not 'model_evaluation':
    from image_capture import setup, take_picture, picam2

# Pre-trained model obtained from https://github.com/JeremyFJ/Shark-Detector
model = tf.saved_model.load('SL_modelv3')

CAPTURED_IMAGES = './captured_images/' # Captured images from the Raspberry Pi camera

threshold = 0.9 # threshold to determine whether image contains a shark or not -- adjust this based on sensitivity

# For model evaluation -------------------------------------------------------------
SHARK_IMG_DIR = './test_images/shark_images/'
NONSHARK_IMG_DIR = './test_images/nonshark_images/'
eval_threshold = 0
true_positive_rates = []
false_positive_rates = []
precision_rates = []
recall_rates = []
true_positives, false_negatives, false_positives, true_negatives = 0, 0, 0, 0
# ----------------------------------------------------------------------------------


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
    global eval_threshold, true_positives, false_negatives, false_positives, true_negatives, true_positive_rates, false_positive_rates, precision_rates, recall_rates
    
    threshold_lst = [x/10 for x in range(0, 11)]
    threshold_lst = threshold_lst[::-1] # Reverse array so we could start with the highest threshold as the first element
    for i in threshold_lst:
        true_positives, false_negatives, false_positives, true_negatives = 0, 0, 0, 0
        eval_threshold = i
        analyze_test_images(SHARK_IMG_DIR, True)
        analyze_test_images(NONSHARK_IMG_DIR, False)
        print(f"TP: {true_positives}      |     FN: {false_negatives}")
        print(f"FP: {false_positives}      |     TN: {true_negatives}")
        print(f"Threshold: {eval_threshold}")
        true_positive_rates.append(true_positives / (true_positives + false_negatives))
        false_positive_rates.append(false_positives / (false_positives + true_negatives))

        try: 
            precision_rates.append(true_positives / (true_positives + false_positives)) # May evaluate to a division by 0 for some threshold values
        except:
            precision_rates.append(0)
        recall_rates.append(true_positives / (true_positives + false_negatives))
        print("--------------------------------------------------------------")
    true_positive_rates = np.array(true_positive_rates)
    false_positive_rates = np.array(false_positive_rates)
    precision_rates = np.array(precision_rates)
    recall_rates = np.array(recall_rates)
    X_Y_Spline = make_interp_spline(false_positive_rates, true_positive_rates)
    false_positive_rates_ = np.linspace(false_positive_rates.min(), false_positive_rates.max(), 500)
    true_positive_rates_ = X_Y_Spline(false_positive_rates_)
    plt.plot(false_positive_rates_, true_positive_rates_)
    plt.show()
    print(true_positive_rates)
    print(false_positive_rates)
    print(precision_rates)
    print(recall_rates)

if 'model_evaluation' in sys.argv: 
    plot_roc()
else:
    setup()
    analyze_captured_input()