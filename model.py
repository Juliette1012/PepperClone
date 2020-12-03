# -*- coding: utf-8 -*-

import pickle
import tensorflow as tf
import numpy as np
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Activation, Flatten, Conv2D, MaxPooling2D, BatchNormalization
from tensorflow.keras.callbacks import EarlyStopping
import tensorflow.keras.layers.experimental.preprocessing as preprocessing

pickle_in = open("X_train.pickle", "rb")
X = pickle.load(pickle_in)
pickle_in.close()

pickle_in = open("y_train.pickle", "rb")
y = pickle.load(pickle_in)
pickle_in.close()

# to normalize we just divide by 255 since we know the values will
# be from 0 to 255
X = X/255.0


# One hot encoding. The data labels must be reformatted in a 3-bit vector
enc = OneHotEncoder()
y = enc.fit_transform(y[:, np.newaxis]).toarray()


early_stopping = EarlyStopping(
    min_delta=0.001, # minimium amount of change to count as an improvement
    patience=5, # how many epochs to wait before stopping
    restore_best_weights=True,
)

# elaborate convnet
model = Sequential()
# data augmentation
model.add(preprocessing.RandomFlip('horizontal')) # flip left-to-right
model.add(preprocessing.RandomContrast(0.5)) # contrast change by up to 50%)

#first convolution layer
model.add(Conv2D(filters=64, kernel_size=3, input_shape=X.shape[1:], activation="relu",
                 padding='same'))
model.add(MaxPooling2D(pool_size=(2,2)))

#second convolution layer
model.add(Conv2D(filters=128, kernel_size=3, activation="relu", padding='same'))
model.add(MaxPooling2D(pool_size=(2,2)))

#third convolution layer
model.add(Conv2D(filters=256, kernel_size=3, activation="relu", padding='same'))
model.add(Conv2D(filters=256, kernel_size=3, activation="relu", padding='same'))
model.add(MaxPooling2D(pool_size=(2,2)))

# Head
# since dense needs a 1D layer and conv2D gives a 2D
model.add(Flatten())
model.add(Dense(units=64, activation='relu'))

model.add(Dense(3,activation='softmax'))


model.compile(loss="categorical_crossentropy",
              optimizer=tf.keras.optimizers.Adam(epsilon=0.01),
              metrics=["accuracy"])

history = model.fit(X, y, batch_size=32, epochs=30, validation_split=0.1)#, callbacks=[early_stopping])

history_frame = pd.DataFrame(history.history)
history_frame.loc[:, ['loss', 'val_loss']].plot()
history_frame.loc[:, ['accuracy', 'val_accuracy']].plot();


#to save the model as a SavedModel file
#model.save('saved_model/my_model')