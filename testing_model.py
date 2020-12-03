# -*- coding: utf-8 -*-

import tensorflow as tf
import pickle
import os
from sklearn.preprocessing import OneHotEncoder
import numpy as np

CURR_DIR = os.getcwd()
my_model = tf.keras.models.load_model(CURR_DIR + '/saved_model/model_3000')

pickle_in = open("X_test.pickle", "rb")
X_test = pickle.load(pickle_in)
pickle_in.close()

pickle_in = open("y_test.pickle", "rb")
y_test = pickle.load(pickle_in)
pickle_in.close()


enc = OneHotEncoder()
y_test = enc.fit_transform(y_test[:, np.newaxis]).toarray()

loss, acc = my_model.evaluate(X_test, y_test, verbose=2)
print('Restored model, accuracy: {:5.2f}%'.format(100 * acc))

#print(my_model.predict(X_test))