import os
import glob
import pandas as pd
import xml.etree.ElementTree as ET

def name_label():
    return ["Car","Stop sign","Traffic sign","Traffic light"]

def xml_to_csv(path):
    xml_list = []
    nameLabel = name_label()
    for nl in nameLabel:
        path_folderLabel = str (path + "/"+ nl)
        print(path_folderLabel)
        for xml_file in glob.glob(path_folderLabel + '/*.xml'):
            tree = ET.parse(xml_file)
            root = tree.getroot()
            for member in root.findall('object'):
                value = (root.find('filename').text,
                        int(root.find('size')[0].text),
                        int(root.find('size')[1].text),
                        member[0].text,
                        int(member[4][0].text),
                        int(member[4][1].text),
                        int(member[4][2].text),
                        int(member[4][3].text)
                        )
                xml_list.append(value)
    column_name = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']
    xml_df = pd.DataFrame(xml_list, columns=column_name)
    return xml_df


def xmlConvertToCsv():
	for folder in ['train','test']:
            path = "Dataset/"+folder
            image_path = os.path.join(path)
            xml_df = xml_to_csv(image_path)	    
            xml_df.to_csv(path + "/Label/" + folder + "_labels.csv", index=None)
            print("Successfully converted " + folder +" xml to csv.")


