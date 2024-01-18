import tensorflow as tf
from tensorflow.keras import datasets, layers, models
from load_data import train_images, train_labels, test_images, test_labels

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
model.save('saved_model/')
print(test_acc)