# -*- coding: utf-8 -*-


from qibullet import SimulationManager
from qibullet import PepperVirtual

import pybullet as p
from threading import Thread
import os
import random
import cv2
import time
import numpy as np
import tensorflow as tf
import pickle
from numpy import asarray
from numpy import savetxt


# camera
class Camera(Thread):
    """This is in this class that every methods related to the cameras are
    scripted."""
    
    def __init__(self, pepper):
        print("CameraThread")
        Thread.__init__(self)
        self.pepper = pepper
    
        
    def save_image(self, image, save_directory):
        #using opencv, we save the image in our database
        done = cv2.imwrite(save_directory, image)
        if (done) :
            #print('image saved to {}'.format(save_directory))
            pass
        else :
            print('problem solving the image')
            pass

    def run(self):
        handle2 = self.pepper.subscribeCamera(PepperVirtual.ID_CAMERA_TOP)
        
        pre_time = time.time()
        dir = os.getcwd()
        standing_data_dir = os.path.join(dir, 'train_database/standing_train_data/')
        crouching_data_dir = os.path.join(dir, 'train_database/crouching_train_data/')
        raising_data_dir = os.path.join(dir, 'train_database/raising_train_data/')
        image_id = 0
        while True:            
            img2 = self.pepper.getCameraFrame(handle2)
            if (time.time() > pre_time + 1):
                #save an image every 0.5 sec
                camRes = self.pepper.getCameraResolution(handle2)
                image_name = "image" + str(image_id)
                image_id += 1
                #self.save_image(img2, raising_data_dir + image_name + ".jpg")
                pre_time = time.time()
                if (image_id > 1000):
                    print(image_id, " images saved succesfully")
                    quit()
                    break;
            cv2.waitKey(1)
            
class CloningBehavior(Thread):
    """This class is used to copy the behavior of a robot based on vision"""
    def __init__(self, pepper):
        print("CloningBehavior")
        Thread.__init__(self)
        self.pepper = pepper
    
    def run(self):
        global canMove
        handle2 = self.pepper.subscribeCamera(PepperVirtual.ID_CAMERA_TOP)
        
        while True :
            if canMove == False :
                img = self.pepper.getCameraFrame(handle2)
                cv2.imshow('ppeepr', img)
                #converting rgb image to gray scale
                r, g, b = img[:,:,0], img[:,:,1], img[:,:,2]
                gray = 0.2989 * r + 0.5870 * g + 0.1140 * b
                gray = np.array(gray).reshape(-1, 320, 240, 1)
                predict = my_model.predict(gray)[0].tolist()
                print(predict)
                if (predict.index(1.0) == 0): #standing
                    pass
                elif (predict.index(1.0) == 1): #crouching
                    self.pepper.goToPosture('Crouch', 1)
                    time.sleep(1)
                    self.pepper.goToPosture('StandZero', 0.5)
                elif (predict.index(1.0) == 2): #raising
                    self.pepper.setAngles('LShoulderPitch', -1.5, 1.0)
                    self.pepper.setAngles('RShoulderPitch', -1.5, 1.0)
                    time.sleep(1)
                    self.pepper.goToPosture('StandZero', 0.5)
                canMove = True
            cv2.waitKey(1)

class AleaMove(Thread):
    """This class gives an aleatory behavior to the pepper. He will move 
    in a defined space and change between 3 postures, from 'StandZero' to
    'Raised' to 'Crouch'."""
    
    def __init__(self, pepper, posture):
            print("AleaMove object initialized")
            Thread.__init__(self)
            self.pepper = pepper
            self.posture = posture
        
    def run(self):
        global canMove
        pre_time = time.time()
        # making the robot move and rotate while staying in a restict zone
        x = -1 + 5 * random.random()
        y = -1 + 2 * random.random()
        theta = -3.14 + 10 * random.random()
        currX, currY, currTheta = self.pepper.getPosition()
        #print("cible : {0:.2f}, {1:.2f}, ".format(x,y))
        while True :            
            #print("cible en {0:.2f}, {1:.2f} atteinte".format(x,y))
            x = -1 + 5 * random.random()
            y = -1 + 2 * random.random()
            theta = -3.14 + 10 * random.random()
            if (time.time() > (pre_time + 5)) and (canMove == True):
                currX, currY, currTheta = self.pepper.getPosition()
                if (abs(currX - x) > 0.1 or abs(currY - y) > 0.1) :
                        self.pepper.moveTo(x,y,theta,1, _async=True)
                #making the robot changing posture every 10 sec
                pre_time = time.time()
                if (self.posture == 'StandZero'):
                    self.pepper.setAngles('LShoulderPitch', -1.5, 1.0)
                    self.pepper.setAngles('RShoulderPitch', -1.5, 1.0)
                    self.posture = 'Raised'
                    time.sleep(2)
                    canMove = False
                elif (self.posture == 'Raised'):
                    self.pepper.goToPosture('Crouch', 0.5)
                    self.posture = 'Crouch'
                    time.sleep(1)
                    canMove = False
                elif (self.posture == 'Crouch'):
                    self.pepper.goToPosture('StandZero', 0.5)
                    self.posture = 'StandZero'
                    time.sleep(1)
                    canMove = False
                else : pass

def ObjectSpawner():
    print("Objectspawner")
    p.connect(p.DIRECT)
    cube_visual = p.createVisualShape(p.GEOM_BOX, halfExtents=[0.125,0.125,0.125])
    cube_collision = p.createCollisionShape(p.GEOM_BOX, halfExtents=[0.25,0.25,0.25])
    cube_body = p.createMultiBody( baseMass=0, baseCollisionShapeIndex=cube_collision,
                                  baseVisualShapeIndex=cube_visual, basePosition = [5,1, 0.725])

    p.loadURDF("./urdf/table/table.urdf", basePosition = [5,1,0], globalScaling = 1)
    p.loadURDF("./urdf/chair/chair.urdf", basePosition = [6,1,0], globalScaling = 1)
    p.loadURDF("./urdf/chair/chair.urdf", basePosition = [7,1,0], globalScaling = 1)


def main():
    global my_model
    global canMove

    # global attribute to replicate a state machine
    canMove = True
    CURR_DIR = os.getcwd()
    my_model = tf.keras.models.load_model(CURR_DIR + '\saved_model\model_3000')
    
    simulation_manager = SimulationManager()
    client_id = simulation_manager.launchSimulation(gui=True)
    pepper = simulation_manager.spawnPepper(client_id,
                                            translation=[-2, 0, 0],
                                            spawn_ground_plane=True)
    
    pepper2 = simulation_manager.spawnPepper(client_id,
                                        translation=[0, 0, 0],
                                        quaternion=[0, 0, -4, 0],
                                        spawn_ground_plane=True)
    
    ObjectSpawner()
    
    #cam = Camera(pepper)
    mover = AleaMove(pepper2, 'StandZero')
    pepClone = CloningBehavior(pepper)
    
    #cam.start()
    mover.start()
    pepClone.start()

    #cam.join()
    mover.join()
    pepClone.join()

main()

    