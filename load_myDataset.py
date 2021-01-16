import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import time

import myPathRepo as pr

path_trainDataset = pr.path_trainDataset()
path_testDataset = pr.path_testDataset()
path_trainDatasetLabel = pr.path_trainDatasetLabel()
path_testDatasetLabel =  pr.path_testDatasetLabel() 

# read one file Label
def readFile(path):
    f = open(path, 'r')
    lignes = f.readlines()
    delimiteur = " "
    L = []
    for ligne in lignes :
        ligne = ligne.replace("\n","")
        l = ligne.split(" ")
        lenght = len(l) 
        rectangle = [int(float(x)) for x in l[-4:] ]
        label =l[(-lenght):(-lenght+(lenght-4))]
        label = delimiteur.join(label)
        #L.append((label,rectangle))
        L.append(rectangle)
    f.close()
    return label, L

##########################
###############"
# "
def load_img(path = path_trainDataset,echantillon=None):
    ### return L [ tuples(img, label_img, L[[rectangle],...], height, width), .... ]
    Liste = []
    for path_dataset in path :
        for file_name in os.listdir(path_dataset)[:echantillon]:
            if file_name.split(".")[-1].lower() in {"jpeg", "jpg", "png"}:
            
                file_path_label = path_dataset + "Label/"  + file_name.split(".")[0]+".txt"
                file_path_image = path_dataset + file_name
            
                data_file_txt = readFile(file_path_label)
                img = cv2.imread(file_path_image)
                height, width, channels = img.shape
                Liste.append((img,data_file_txt[0],data_file_txt[1],height,width))

                        
    return Liste


#Liste.append(image,label,[coord],height,width)
# load the masks for an image
def load_mask(path = path_trainDataset,echantillon=None):
    Liste_img = load_img(path,echantillon)
    class_ids = list()
    for i in Liste_img:
        masks = np.zeros([i[3],i[4]], dtype='uint8')
        for j in range(len(i[2])):
            box = i[2][j]
            row_s, row_e = box[1], box[3]
            col_s, col_e = box[0], box[2]
            masks[row_s:row_e, col_s:col_e] = 1
        class_ids.append((i,masks))
    return class_ids

def load_dataset(path = path_trainDataset,echantillon=None):
    data = load_mask(path,echantillon)
    df = pd.DataFrame(columns=["image","label","rectangle","height","width","mask"])
    for d in data:
        df = df.append({'image':d[0][0],'label':d[0][1],'rectangle':d[0][2],'height':d[0][3],"width":d[0][4],"mask":d[1]}, ignore_index=True)
    return df   


#################################################
####################"
# 
def show_data(data):
    if(type(data) is pd.DataFrame):
        show_dataframe(data)
    elif (type(data[0][1]) is str):
        show_image(data)
    elif(type(data[0][1]) is np.ndarray  ):
        show_mask(data)
    else :
        print("error")

def show_mask(liste_mask):
    cp_mask = liste_mask.copy()
    for img in cp_mask :
        img[1][img[1]==1]=255
        window_name = "Visualizer"
        cv2.imshow(window_name, img[1])
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
        
def show_image(liste_img):
    index=0
    r,g,b = 255 , 0,0
    for img in liste_img : 
        index = index+1
        window_name = "Visualizer: {}/{}".format(index, len(data_train))
        show_oneImage(img[0],img[2],name=window_name)

def show_dataframe(df):
    for i in range(len(df)):
        image = df.loc[i,"image"]
        rectangle = df.loc[i,"rectangle"]
        window_name = "Visualizer: {}/{}".format(i, len(df))
        show_oneImage(image,rectangle,name=window_name)

def show_oneImage(img,rectangle,color=(255,0,0), name="1/1"):
    for ax in rectangle:   
            cv2.rectangle(img, (ax[-2],ax[-1]),(ax[-4],ax[-3]), color, 3)
    cv2.imshow(name, img)
    cv2.waitKey(0)
    # We close the window
    cv2.destroyAllWindows()