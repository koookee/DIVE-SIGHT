'''
Evaluates the performance of the model and plots different performance 
metrics. Pass "exisiting_data" as an argument to the script if the confusion 
matrix data has already been aquired and bypass evaluating the model on the test 
images
'''

import matplotlib.pyplot as plt
import numpy as np
import sys
import os
import cv2

if 'existing_data' not in sys.argv: 
    from load_model import model, analyze_image

thresholds = [1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 0.0]
true_positive_rates = []
false_positive_rates = []
precision_rates = []
recall_rates = []

if 'existing_data' in sys.argv: 
    # In descending order of the threshold values
    true_positives = [0, 554, 595, 608, 618, 624, 629, 632, 636, 636, 637]
    false_negatives = [637, 83, 42, 29, 19, 13, 8, 5, 1, 1, 0]
    false_positives = [0, 482, 905, 1205, 1513, 1825, 2188, 2640, 3236, 3983, 4305]
    true_negatives = [4305, 3823, 3400, 3100, 2792, 2480, 2117, 1665, 1069, 322, 0]
else: 
    SHARK_IMG_DIR = './test_images/shark_images/'
    NONSHARK_IMG_DIR = './test_images/nonshark_images/'
    true_positives = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    false_negatives = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    false_positives = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    true_negatives = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]


def analyze_test_images(IMG_DIR, is_shark, eval_threshold, index):
    """
    Analyzes test images to fill the confusion matrix at different 
    threshold values

    Args:
        IMG_DIR (str): Directory path of the images.
        is_shark (bool): Flag indicating if the images contain a shark.
        eval_threshold (float): Evaluation threshold.
        index (int): Index of the threshold.

    Returns:
        None
    """
    for img in os.listdir(IMG_DIR): # iterate through each image in the image directory
        img_name = img.split(".")[0]
        img = cv2.imread(IMG_DIR + img)
        confidence = analyze_image(img)
        predicted_shark = confidence > eval_threshold # True if the model predicted that the image contains a shark; false otherwise
        if (predicted_shark) and is_shark:
            true_positives[index] += 1
        elif (not predicted_shark) and is_shark:
            false_negatives[index] += 1
        elif (predicted_shark) and not is_shark:
            false_positives[index] += 1
        elif (not predicted_shark) and not is_shark:
            true_negatives[index] += 1

def to_numpy_arrays():
    """
    Converts lists to NumPy arrays.
    """
    global true_positive_rates, false_positive_rates, precision_rates, recall_rates, thresholds
    true_positive_rates = np.array(true_positive_rates)
    false_positive_rates = np.array(false_positive_rates)
    precision_rates = np.array(precision_rates)
    recall_rates = np.array(recall_rates)
    thresholds = np.array(thresholds)

    
def plot_f1_threshold():
    """
    Plots F1 score vs Threshold.
    """
    f1_scores = 2 * (precision_rates * recall_rates) / (precision_rates + recall_rates)
    max_f1_index = np.argmax(f1_scores)
    plt.plot(thresholds, f1_scores)
    plt.xlabel('Threshold')
    plt.ylabel('F1 Score')
    plt.title('F1 Score vs Threshold')
    plt.grid(True)
    plt.ylim(0, 1)
    plt.annotate(f'Max F1 Score = {f1_scores[max_f1_index]:.2f}\nThreshold = {thresholds[max_f1_index]:.2f}',
             xy=(thresholds[max_f1_index], f1_scores[max_f1_index]),
             xytext=(thresholds[max_f1_index] - 0.4, f1_scores[max_f1_index]),
             fontsize=10)
    plt.show()

def plot_ROC():
    """
    Plots Receiver Operating Characteristic (ROC) curve.
    """
    auc = np.trapz(true_positive_rates, false_positive_rates)
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('ROC Curve')
    plt.plot([0, 1], [0, 1], linestyle='--', color='gray')
    plt.annotate(f'AUC = {auc:.2f}', xy=(0.6, 0.4), xytext=(0.7, 0.6),
             fontsize=12)
    plt.plot(false_positive_rates, true_positive_rates)
    plt.grid(True)
    plt.show()

def plot_PR():
    """
    Plots Precision-Recall curve.
    """
    plt.plot(recall_rates, precision_rates)
    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.title('Precision-Recall Curve')
    plt.grid(True)
    plt.show()

def print_confusion_matrix(index):
    """
    Prints confusion matrix.

    Args:
        index (int): Index of the threshold.

    Returns:
        None
    """
    print(f"TP: {true_positives[index]}      |     FN: {false_negatives[index]}")
    print(f"FP: {false_positives[index]}      |     TN: {true_negatives[index]}")
    print(f"Threshold: {thresholds[index]}")
    print("--------------------------------------------------------------")
    
def calculate_tpr_fpr():
    """
    Calculates True Positive Rates (TPR) and False Positive Rates (FPR) for each threshold
    """
    for index in range (0, len(thresholds)):
        true_positive_rates.append(true_positives[index] / (true_positives[index] + false_negatives[index]))
        false_positive_rates.append(false_positives[index] / (false_positives[index] + true_negatives[index]))

def calculate_precision_recall():
    """
    Calculates Precision and Recall rates for each threshold
    """
    for index in range (0, len(thresholds)):
        if true_positives[index] == 0 and false_positives[index] == 0: 
            precision_rates.append(1)
        else:
            precision_rates.append(true_positives[index] / (true_positives[index] + false_positives[index]))

        recall_rates.append(true_positives[index] / (true_positives[index] + false_negatives[index]))

if 'existing_data' not in sys.argv: 
    for index, threshold in enumerate(thresholds):
        analyze_test_images(SHARK_IMG_DIR, True, threshold, index)
        analyze_test_images(NONSHARK_IMG_DIR, False, threshold, index)

calculate_tpr_fpr()
calculate_precision_recall()
to_numpy_arrays()

for index in range (0, len(thresholds)):
    print_confusion_matrix(index)

plot_ROC()
plot_PR()
plot_f1_threshold()
