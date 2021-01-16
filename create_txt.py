
import numpy as np

def listePositif(liste,n):
    for el in liste :
        if el < n :
            return False
    return True
       

def listeCompriseInImage(rectangle,height, width):
    if (rectangle[1]< height) and (rectangle[3]< height) and (rectangle[0]< width) and (rectangle[2]< width):
        return True
    else :
        return False

def xy_min(x1,x2):
    if x1>x2 :
        return x2,x1
    else :
        return x1,x2


def write_txt(label,rectangle,nameFile ,height, width):
    a = 0
    rectangle = (np.array(rectangle)).astype(float).tolist()
    with open(nameFile, "w") as filout:
        for rec in rectangle:
            if listePositif(rec,1) and listeCompriseInImage(rec,height, width):
                x_min,x_max = xy_min(rec[0],rec[2])
                y_min,y_max = xy_min(rec[1],rec[3])
                word =("{} {}  {}  {}  {}\n".format(label, x_min ,y_min,x_max,y_max).encode('ascii', 'ignore')).decode('ascii')
                filout.write(word)
                a = 1
    if a == 1:
        return True
    else:
        return False
            
            