from tensorflow import keras
import matplotlib.pyplot as plt
from load_data import test_images, test_labels, input_images, input_labels, CATEGORIES

model = keras.models.load_model('saved_model/')
                    
test_loss, test_acc = model.evaluate(test_images,  test_labels, verbose=2)

predictions = model.predict(input_images)

for idx, pred in enumerate(predictions):
  plt.imshow(input_images[idx] ,cmap=plt.cm.binary)
  print(pred)
  print(f"Actual: {CATEGORIES[input_labels[idx]]}")
  print(f"Prediction: {CATEGORIES[pred.argmax()]}")
  #plt.show()
  print("--------------------------------------------------------------------------")