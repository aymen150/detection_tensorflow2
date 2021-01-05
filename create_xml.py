import cv2
import xml.etree.cElementTree as ET
import myPathRepo as pr
import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import time
import load_myDataset as lmd

#path_repo = "/home/aymen/Documents/OIDv4_ToolKit-master/OID"


def create_xml(tOt,path,filename,width,height,label,rectangle):
    save = str(filename.split('.')[0])
    print(save)
    root = ET.Element("annotation")
    #
    ET.SubElement(root, "folder").text = str(tOt)
    ET.SubElement(root, "filename").text = filename
    ET.SubElement(root, "path").text = path +  filename
    source = ET.SubElement(root, "source")
    ##
    ET.SubElement(source, "database").text = "Unknown"
    #
    size = ET.SubElement(root, "size")
    ##
    ET.SubElement(size, "width").text = str(width)
    ET.SubElement(size, "height").text = str(height)
    ET.SubElement(size, "depth").text = "3"
    #
    ET.SubElement(root, "segmented").text = "0"
    
    for r in rectangle:
        obj = ET.SubElement(root, "object")
        ##
        ET.SubElement(obj, "name").text = label
        ET.SubElement(obj, "pose").text = "Unspecified"
        ET.SubElement(obj, "truncated").text = 0
        ET.SubElement(obj, "difficult").text = 0
        box = ET.SubElement(obj, "bndbox")
        ###
        ET.SubElement(box, "xmin").text = str(r[1])
        ET.SubElement(box, "ymin").text = str(r[0])
        ET.SubElement(box, "xmax").text = str(r[3])
        ET.SubElement(box, "ymax").text = str(r[2])
        

    tree = ET.ElementTree(root)
    tree.write(path+save+".xml")
    
#path_label = "/home/aymen/Documents/OIDv4_ToolKit-master/OID/Dataset/train/Traffic sign/Label/"

def create_xmlFile():
    for tOt in ["train","test"]:        
        liste_repo_img = pr.path_defineDataset(tOt)
        for path_dataset in liste_repo_img:
            path_label = path_dataset + "Label/"
            print(path_dataset)
            for file_name in os.listdir(path_dataset):
                if file_name.split(".")[-1].lower() in {"jpeg", "jpg", "png"}:
                
                    file_path_label = path_label + file_name.split(".")[0]+".txt"
                    file_path_image = path_dataset + file_name
                
                    data_file_txt = lmd.readFile(file_path_label)
                    img = cv2.imread(file_path_image)
                    height, width, channels = img.shape
                    create_xml(tOt,path_dataset,file_name,width,height,data_file_txt[0],data_file_txt[1])