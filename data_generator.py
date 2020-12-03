# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import os 
import cv2

CURR_DIR = os.getcwd()
DATADIR = os.path.join(CURR_DIR, 'test_database/')
CATEGORIES = ["standing_test_data", "crouching_test_data", "raising_test_data"]

#image are store in jpg of 320x240

# rescaling the image fore best performance ?
#IMG_SIZE = 100


training_data = []
def create_data():
    for category in CATEGORIES:
        path = os.path.join(DATADIR, category) # path to the three sets of data
        class_num = CATEGORIES.index(category) #giving 0 for standing, 1 for crouching and 2 for raising
        for img in os.listdir(path):
            try :
                # we convert to gray scale because colors aren't necessary to differentiate pepper's posture 
                img_array = cv2.imread(os.path.join(path,img), cv2.IMREAD_GRAYSCALE)
                #new_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))
                training_data.append([img_array, class_num])
            except Exception as e:
                print("Problem in the image {} : {}".format(img, e))
                pass
create_data()

import random
random.shuffle(training_data)

# split data and label
X = []
y = []

for features, label in training_data:
    X.append(features)
    y.append(label)
X = np.array(X).reshape(-1, 240, 320, 1)
y = np.array(y)

# saving the X and y with pickle to be used in our model
import pickle
pickle_out = open("X_test.pickle", "wb")
pickle.dump(X, pickle_out)
pickle_out.close()
print("X saved in 'X_test.pickle' with shape " , X.shape)

pickle_out = open("y_test.pickle", "wb")
pickle.dump(y, pickle_out)
pickle_out.close()
print("y saved in 'y_test.pickle'")
