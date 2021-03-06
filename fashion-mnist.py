# -*- coding: utf-8 -*-
"""Untitled2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1yqVX9_Lkzyby8l8BYEYxxwgkR-Wxhe--

Installing required packages
"""

!pip install -U tensorflow_datasets

import tensorflow as tf

# Import TensorFlow Datasets
import tensorflow_datasets as tfdt
tfdt.disable_progress_bar()

# Helper libraries
import math
import numpy as ny
import matplotlib.pyplot as pt

"""For showing the error if any"""

import logging
logger = tf.get_logger()
logger.setLevel(logging.ERROR)

"""Downloading and importing fashion mnist dataset that contains 70k gray scaled images of size 28x28 pixel each. out of which 60k images are used for training the model and rest 10k are used for testing the model and it is a classification based problem.In which it contains 10 categories  and their outputs are labelled as (0,1,2,...,9).In which:
0	T-shirt/top
1	Trouser
2	Pullover
3	Dress
4	Coat
5	Sandal
6	Shirt
7	Sneaker
8	Bag
9	Ankle boot

"""

dataset, metadata = tfdt.load('fashion_mnist', as_supervised=True, with_info=True)
train_ds, test_ds = dataset['train'], dataset['test']

classNames = metadata.features['label'].names
print("Class names: {}".format(classNames))

"""number of training examples and number of test examples

no_of_train_examples = metadata.splits['train'].no_of_examples
no_of_test_examples = metadata.splits['test'].no_of_examples
print("Number of training examples: {}".format(no_of_train_examples))
print("Number of test examples:     {}".format(no_of_test_examples))
"""

no_of_train_examples = metadata.splits['train'].num_examples
no_of_test_examples = metadata.splits['test'].num_examples
print("Number of training examples: {}".format(no_of_train_examples))
print("Number of test examples:     {}".format(no_of_test_examples))

"""**PREPROCESSING THE DATA**
every pixel value in the image data is an integer in the range [0,255]. For the model to work properly, these values need to be normalized to the range [0,1]. So here we create a normalization function,and apply the normalization to all the images.
"""

def normalization(images, labels):
  images = tf.cast(images, tf.float32)
  images /= 255
  return images, labels

train_ds =  train_ds.map(normalization)
test_ds  =  test_ds.map(normalization)


train_ds =  train_ds.cache()
test_ds  =  test_ds.cache()

"""Showing the images after preprocessing with some examples"""

for image, label in test_ds.take(1):
  break
image = image.numpy().reshape((28,28))

# Plot the image - voila a piece of fashion clothing
pt.figure()
pt.imshow(image, cmap=pt.cm.binary)
pt.colorbar()
pt.grid(False)
pt.show()

pt.figure(figsize=(10,10))
for i, (image, label) in enumerate(train_ds.take(25)):
    image = image.numpy().reshape((28,28))
    pt.subplot(5,5,i+1)
    pt.xticks([])
    pt.yticks([])
    pt.grid(False)
    pt.imshow(image, cmap=pt.cm.binary)
    pt.xlabel(classNames[label])
pt.show()

"""**NOW WE ARE READY WITH OUR DATASET WE WILL NOW BUILD A MODEL WITH THRE LAYERS**
HERE WE WILL BE USING FLATTEN FUNCTION TO MAKE THE MATRIX INPUT INTO A SINGLE COLUMN MATRIX AND AFTER THAT WE WILL USE RELU FUNCTION WHICH IS MOST POWERFUL FUNCTION COMPARED TO SIGMOID,LINEAR FUNCTIONS.AND THEN FINALLY WE WILL USE A SOFTMAX FUNCTION TO GET THE PROBABILITY EACH AND EVERY LABEL. FINALLY WE WILL CONSIDER THE ONE WITH MAXMIMUM PROBABILITY.
"""

model = tf.keras.Sequential([
    tf.keras.layers.Flatten(input_shape=(28, 28, 1)),
    tf.keras.layers.Dense(128, activation=tf.nn.relu),
    tf.keras.layers.Dense(10, activation=tf.nn.softmax)
])

"""# **WE WILL COMPILE THE MODEL USING ADAM OPTIMIZER**"""

model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(),
              metrics=['accuracy'])

"""NOW WE WILL TRAIN OUR MODEL WITH A BATCH SIZE OF 32"""

BATCH_SIZE = 32
train_ds = train_ds.cache().repeat().shuffle(no_of_train_examples).batch(BATCH_SIZE)
test_ds = test_ds.cache().batch(BATCH_SIZE)

model.fit(train_ds, epochs=1, steps_per_epoch=math.ceil(no_of_train_examples/BATCH_SIZE))

"""# **NOW WE WILL CHECK FOR ACCCURACY**"""

test_loss, test_accuracy = model.evaluate(test_ds, steps=math.ceil(no_of_test_examples/32))
print('Accuracy on test ds:', test_accuracy)

for test_images, test_labels in test_ds.take(1):
  test_images = test_images.numpy()
  test_labels = test_labels.numpy()
  predictions = model.predict(test_images)

predictions.shape

predictions[0]

ny.argmax(predictions[0])

test_labels[0]

def plot_image(i, predictions_array, true_labels, images):
  predictions_array, true_label, img = predictions_array[i], true_labels[i], images[i]
  pt.grid(False)
  pt.xticks([])
  pt.yticks([])
  
  pt.imshow(img[...,0], cmap=pt.cm.binary)

  predicted_label = ny.argmax(predictions_array)
  if predicted_label == true_label:
    color = 'blue'
  else:
    color = 'red'
  
  pt.xlabel("{} {:2.0f}% ({})".format(classNames[predicted_label],
                                100*ny.max(predictions_array),
                                classNames[true_label]),
                                color=color)

def plot_value_array(i, predictions_array, true_label):
  predictions_array, true_label = predictions_array[i], true_label[i]
  pt.grid(False)
  pt.xticks([])
  pt.yticks([])
  thisplot = pt.bar(range(10), predictions_array, color="#777777")
  pt.ylim([0, 1]) 
  predicted_label = ny.argmax(predictions_array)
  
  thisplot[predicted_label].set_color('red')
  thisplot[true_label].set_color('blue')

i = 0
pt.figure(figsize=(6,3))
pt.subplot(1,2,1)
plot_image(i, predictions, test_labels, test_images)
pt.subplot(1,2,2)
plot_value_array(i, predictions, test_labels)

i = 12
pt.figure(figsize=(6,3))
pt.subplot(1,2,1)
plot_image(i, predictions, test_labels, test_images)
pt.subplot(1,2,2)
plot_value_array(i, predictions, test_labels)

num_rows = 5
num_cols = 3
num_images = num_rows*num_cols
pt.figure(figsize=(2*2*num_cols, 2*num_rows))
for i in range(num_images):
  pt.subplot(num_rows, 2*num_cols, 2*i+1)
  plot_image(i, predictions, test_labels, test_images)
  pt.subplot(num_rows, 2*num_cols, 2*i+2)
  plot_value_array(i, predictions, test_labels)

img = test_images[0]

print(img.shape)

img = ny.array([img])

print(img.shape)

predictions_single = model.predict(img)

print(predictions_single)

plot_value_array(0, predictions_single, test_labels)
_ = pt.xticks(range(10), classNames, rotation=45)

ny.argmax(predictions_single[0])