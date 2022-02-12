"""
Pontificia Universidad Javeriana
Departamento de electrónica
TG1907
Objetivo 1: Calibración de color

@author: David Felipe Cuellar Diaz
"""

import calibracionColor
import os

directory = os.getcwd()

folder= directory + "/results/"

checker= directory + "/CCi13_2.jpg"
warpedout= folder + "warped14_2.png"
checkerout= folder + "CCD14_2.png"
de= folder + "DEColD14_2.png"
dechg= folder + "DEBPD14_2.png"
matrix= folder + "matrix14_2.txt"

print(checker)
print("Hello World! Welcome to Python Examples.")


cc=calibracionColor.imagenes(checker=checker,scalefactor=1,checkerout=checkerout,warpedout=warpedout,de=de,dechg=dechg,matrix=matrix)

cc.checkerCalibration()

#cc.imageCalibration()

