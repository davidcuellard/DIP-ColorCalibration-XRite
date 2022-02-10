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

folder= directory + "/DIP-ColorCalibration-XRite/"

#checker= folder + "drone0/CCiD_0.png"
#warpedout= folder + "drone0/warped_1.png"
#checkerout= folder + "drone0/CCD_1.png"
#de= folder + "drone0/DEColD_1.png"
#dechg= folder + "drone0/DEBPD_1.png"
#matrix= folder + "drone0/matrix_1.txt"

#checker= folder + "drone0/CCiD_0.png"
#warpedout= folder + "drone0/warped_2.png"
#checkerout= folder + "drone0/CCD_2.png"
#de= folder + "drone0/DEColD_2.png"
#dechg= folder + "drone0/DEBPD_2.png"
#matrix= folder + "drone0/matrix_2.txt"


#
#checker= folder + "drone12/CCiD_1.png"
#warpedout= folder + "drone12/warped_1.png"
#checkerout= folder + "drone12/CCD_1.png"
#de= folder + "drone12/DEColD_1.png"
#dechg= folder + "drone12/DEBPD_1.png"
#matrix= folder + "drone12/matrix_1.txt"
#
#checker= folder + "drone12/CCiD_2.png"
#warpedout= folder + "drone12/warped_2.png"
#checkerout= folder + "drone12/CCD_2.png"
#de= folder + "drone12/DEColD_2.png"
#dechg= folder + "drone12/DEBPD_2.png"
#matrix= folder + "drone12/matrix_2.txt"

#checker= folder + "10/CCi10_1.jpg"
#warpedout= folder + "10/warped10_1.png"
#checkerout= folder + "10/CCD10_1.png"
#de= folder + "10/DEColD10_1.png"
#dechg= folder + "10/DEBPD10_1.png"
#matrix= folder + "10/matrix10_1.txt"

#checker= folder + "10/CCi10_2.jpg"
#warpedout= folder + "10/warped10_2.png"
#checkerout= folder + "10/CCD10_2.png"
#de= folder + "10/DEColD10_2.png"
#dechg= folder + "10/DEBPD10_2.png"
#matrix= folder + "10/matrix10_2.txt"

#checker= folder + "11/CCi11_1.jpg"
#warpedout= folder + "11/warped11_1.png"
#checkerout= folder + "11/CCD11_1.png"
#de= folder + "11/DEColD11_1.png"
#dechg= folder + "11/DEBPD11_1.png"
#matrix= folder + "11/matrix11_1.txt"

#checker= folder + "11/CCi11_2.jpg"
#warpedout= folder + "11/warped11_2.png"
#checkerout= folder + "11/CCD11_2.png"
#de= folder + "11/DEColD11_2.png"
#dechg= folder + "11/DEBPD11_2.png"
#matrix= folder + "11/matrix11_2.txt"

#checker= folder + "12/CCi12_1.jpg"
#warpedout= folder + "12/warped12_1.png"
#checkerout= folder + "12/CCD12_1.png"
#de= folder + "12/DEColD12_1.png"
#dechg= folder + "12/DEBPD12_1.png"
#matrix= folder + "12/matrix12_1.txt"

#checker= folder + "12/CCi12_2.jpg"
#warpedout= folder + "12/warped12_2.png"
#checkerout= folder + "12/CCD12_2.png"
#de= folder + "12/DEColD12_2.png"
#dechg= folder + "12/DEBPD12_2.png"
#matrix= folder + "12/matrix12_2.txt"

#checker= folder + "13/CCi13_1.jpg"
#warpedout= folder + "13/warped13_1.png"
#checkerout= folder + "13/CCD13_1.png"
#de= folder + "13/DEColD13_1.png"
#dechg= folder + "13/DEBPD13_1.png"
#matrix= folder + "13/matrix13_1.txt"

#checker= folder + "13/CCi13_2.jpg"
#warpedout= folder + "13/warped13_2.png"
#checkerout= folder + "13/CCD13_2.png"
#de= folder + "13/DEColD13_2.png"
#dechg= folder + "13/DEBPD13_2.png"
#matrix= folder + "13/matrix13_2.txt"

#checker= folder + "14/CCi14_1.jpg"
#warpedout= folder + "14/warped14_1.png"
#checkerout= folder + "14/CCD14_1.png"
#de= folder + "14/DEColD14_1.png"
#dechg= folder + "14/DEBPD14_1.png"
#matrix= folder + "14/matrix14_1.txt"

checker= folder + "CCi13_2.jpg"
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

