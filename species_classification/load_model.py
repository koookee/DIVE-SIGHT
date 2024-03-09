'''
Loads in the shark detector model and provides the function to analyze an image and 
return a confidence score for the presence of sharks 
'''

import tensorflow as tf
import sys

# Pre-trained model obtained from https://github.com/JeremyFJ/Shark-Detector
model = tf.saved_model.load('SL_modelv3')

def analyze_image(image_np):
    """
    Returns a confidence score for whether an image contains a shark or not

    Args:
        image_np (numpy array): a numpy array of the image

    Returns:
        int: the confidence score
    """
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
        