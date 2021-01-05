
import numpy as np

def listePositif(liste,n):
    for el in liste :
        if el < n :
            return False
    return True
        

def write_txt(label,rectangle,nameFile ):
    a = 0
    rectangle = (np.array(rectangle)).astype(float).tolist()
    with open(nameFile, "w") as filout:
        for rec in rectangle:
            if listePositif(rec,-20):
                word =("{} {}  {}  {}  {}\n".format(label, rec[0],rec[1],rec[2],rec[3]).encode('ascii', 'ignore')).decode('ascii')
                filout.write(word)
                a = 1
    if a == 1:
        return True
    else:
        return False
            
            