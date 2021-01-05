import os
import cv2
import numpy as np

def path_AllDataset():
    return path_trainDataset() + path_testDataset()

def path_trainDataset() :
    return ["Dataset/train/Traffic sign/","Dataset/train/Stop sign/","Dataset/train/Traffic light/","Dataset/train/Car/"]

def path_testDataset() :
    return ["Dataset/test/Traffic sign/", "Dataset/test/Stop sign/","Dataset/test/Traffic light/","Dataset/test/Car/"]

def path_trainDatasetLabel():
    return ["Dataset/train/Traffic sign/Label","Dataset/train/Stop sign/Label","Dataset/train/Traffic light/Label","Dataset/train/Car/Label"]

def path_testDatasetLabel() :
    return ["Dataset/test/Traffic sign/Label", "Dataset/test/Stop sign/Label","Dataset/test/Traffic light/Label","Dataset/test/Car/Label"]

def path_RacineDataset():
    return "Dataset/"

def path_dicoDataset(tpe="train"):
    if (tpe == "train") :
        return {"Traffic sign" : path_trainDataset()[0], "Stop sign" :path_trainDataset()[1], "Traffic light" : path_trainDataset()[2] , "Car" : path_trainDataset()[3] }
    elif (tpe == "test") :
        return {"Traffic sign" : path_testDataset()[0], "Stop sign" :path_testDataset()[1], "Traffic light" : path_testDataset()[2] , "Car" : path_testDataset()[3] }
    else :
        print("error name") 
        return {}
    
def path_oneDataset(name,tpe="train"):
    print(path_dicoDataset(tpe)[name])
    return [path_dicoDataset(tpe)[name]]

def path_defineDataset(tOt):
    if (tOt == "train"):
        return path_trainDataset()
    elif (tOt == "test"):
        return path_testDataset()
    else:
        print("ERROR valeur paramétre. option 1: train or 2: test")
        return []