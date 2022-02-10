"""
Pontificia Universidad Javeriana
Departamento de electrónica
Proyecto OMICAS
TG1907
Objetivo 1: Calibración de color
@author: David Felipe Cuellar Diaz
"""

#Importar los paquetes necesarios
import numpy as np
import cv2
from PIL import Image
import matplotlib.pyplot as plt

class imagenes:
    
    def __init__(self,checker="colorchecker1.jpeg",scalefactor=1,warpedout="warped.bmp",checkerout="cchecker.bmp",de='DistanciaEuclideaColores.png',dechg='DistanciaEuclideaBoxplot.png',image="colorchecker1.jpeg",imageout="cimage.bmp",scalefactor2=1,matrix="",matriximg=""):
        self.checker=checker
        self.scalefactor=scalefactor
        self.warpedout=warpedout
        self.checkerout=checkerout
        self.de=de
        self.dechg=dechg
        self.matrix=matrix
        self.image=image
        self.imageout=imageout
        self.scalefactor2=scalefactor2
        self.matriximg=matriximg

        self.alphasmean=0
        self.puntos=0
        self.x1=0
        self.x2=0
        self.x3=0
        self.x4=0
        self.y1=0
        self.y2=0
        self.y3=0
        self.y4=0
    
    #Defiir algunas funciones
    #Definir las coordenadas para la transformación de perspectiva
    def order_points(self,pts):
    # inicializa una lista de coordenadas que serán ordenadas
    # La primera coordenada debe ser el la esquina en el color "dark skin"
    # Sigue tomando los puntos en el sentido de las manecillas del reloj
        rect = np.zeros((4, 2), dtype = "float32")
        # EL primer punto debe tener la suma más pequeña  	
     # EL tercer punto debe tener la suma más grande
        s = pts.sum(axis = 1)
        rect[0] = pts[np.argmin(s)]
        rect[2] = pts[np.argmax(s)]
     
    # Se calcula la diferencia entre los puntos
        diff = np.diff(pts, axis = 1)
        rect[1] = pts[np.argmin(diff)]
        rect[3] = pts[np.argmax(diff)]
     
        # devuelve las coordenadas ordenadas
        return rect

    #Transformación de perspectiva    
    def four_point_transform(self,image, pts):
    #Toma las coordenadas ordenadas
        (tl, tr, br, bl) = pts
        rect=pts

    # Calcula el ancho de la nueva imagen, la cual será la distancia máxima entre 
    # los dos útlimos puntos de las coordenadas ordenadas
        widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
        widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
        maxWidth = max(int(widthA), int(widthB))
     
 
    # Calcula la altura de la nueva imagen, la cual será la distancia máxima entre
    # el segundo y el tercer punto de las coordenadas ordenadas	
        heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
        heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
        maxHeight = max(int(heightA), int(heightB))
     
    # Ahora con las dimensiones de la nueva imagen, se construye
    # los puntos destino para obtener una vista de "ojo de pajaro"
        dst = np.array([
            [0, 0],
            [maxWidth - 1, 0],
            [maxWidth - 1, maxHeight - 1],
            [0, maxHeight - 1]], dtype = "float32")
     
        # calcula la matriz de transformada de perspectiva y la aplica
        M = cv2.getPerspectiveTransform(rect, dst)
        warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
     
        # devuelve la imagen recortada
        return warped
    
    # Utiliza esta función para tomar los 4 puntos
    def mousePosition(self,event,x,y,flags,param):
        if event == cv2.EVENT_LBUTTONDOWN:
            print(x,y)
            if self.puntos==0:
                self.x1=x
                self.y1=y
            if self.puntos==1:
                self.x2=x
                self.y2=y
            if self.puntos==2:
                self.x3=x
                self.y3=y
            if self.puntos==3:
                self.x4=x
                self.y4=y
        if event == cv2.EVENT_LBUTTONUP:
            self.puntos=self.puntos+1

    def checkerCalibration(self):
        #Lee la imágen
        image = cv2.imread(self.checker)
        
        #Hace más pequeña la imágen para colocar bien los puntos
        height, width = image.shape[:2]
        image = cv2.resize(image,(int(self.scalefactor*width), int(self.scalefactor*height)), interpolation = cv2.INTER_NEAREST)
        cv2.imshow("Original", image)
        
        #Elegir los cuatro puntos empezando en la ezquina superior izquierda y en sentido horario
        #Tomar los eventos de click del mouse
        #Basado en: https://www.pyimagesearch.com/2015/03/09/capturing-mouse-click-events-with-python-and-opencv/
        print('Elija los cuatro puntos, empezando en la esquina color café en sentido horario')
        while self.puntos<4:
            cv2.waitKey(1) & 0xFF    
            cv2.setMouseCallback('Original',self.mousePosition) 
        
        #Transformación de perspectiva del tablero
        #Basado en: Francisco Calderon. Clase: Procesamiento de imagenes y visión
        pts = np.array([(self.x1, self.y1), (self.x2,self.y2), (self.x3,self.y3), (self.x4, self.y4)], dtype = "float32")   
        
        # Aplica la transformada de perspectiva a los cuatro puntos elegidos con el mouse
        warped = self.four_point_transform(image, pts)    
        size = (810, 543)
        warped = cv2.resize(warped, size, interpolation = cv2.INTER_AREA)
    
        #Guarda la imagen recortada
        cv2.imwrite(self.warpedout ,warped)
        
        #Se tiene la siguiente ecuación
        #x=(((A^T)A)⁻1)(A^T)(b)
             
        #Se define la matriz B de los valores de referencia del color Checker
        
        #dark skin
        rr0,gr0,br0=116,81,67
        #light skin
        rr1,gr1,br1=199,147,129
        #blue sky
        rr2,gr2,br2=91,122,156
        #foliage
        rr3,gr3,br3=90,108,64
        #blue flower
        rr4,gr4,br4=130,128,176
        #bluish green
        rr5,gr5,br5=92,190,172
        
        #orange
        rr6,gr6,br6=224,124,47
        #purplish blue
        rr7,gr7,br7=68,91,170
        #moderate red
        rr8,gr8,br8=198,82,97
        #purple
        rr9,gr9,br9=94,58,106
        #yellow green
        rr10,gr10,br10=159,189,63
        #orange yellow
        rr11,gr11,br11=230,162,39

        #blue
        rr12,gr12,br12=35,63,147
        #green
        rr13,gr13,br13=67,149,74
        #red
        rr14,gr14,br14=180,49,57
        #yellow
        rr15,gr15,br15=238,198,20
        #magenta
        rr16,gr16,br16=193,84,151
        #cyan        
        rr17,gr17,br17=0,136,170
        
        #white 9.5 (.05 D)
        rr18,gr18,br18=245,245,243
        #neutral 8 (.23 D)
        rr19,gr19,br19=200,202,202
        #neutral 6.5 (.44 D)
        rr20,gr20,br20=161,163,163
        #neutral 5 (.70 D)
        rr21,gr21,br21=121,121,122
        #neutral 3.5 (1.05 D)
        rr22,gr22,br22=82,84,86
        #black 2 (1.5 D)
        rr23,gr23,br23=49,49,51
        
        
        b =[[ rr0 ],[ gr0 ],[ br0 ],
            [ rr1 ],[ gr1 ],[ br1 ],
            [ rr2 ],[ gr2 ],[ br2 ],
            [ rr3 ],[ gr3 ],[ br3 ],
            [ rr4 ],[ gr4 ],[ br4 ],
            [ rr5 ],[ gr5 ],[ br5 ],
            [ rr6 ],[ gr6 ],[ br6 ],
            [ rr7 ],[ gr7 ],[ br7 ],
            [ rr8 ],[ gr8 ],[ br8 ],
            [ rr9 ],[ gr9 ],[ br9 ],
            [ rr10 ],[ gr10 ],[ br10 ],
            [ rr11 ],[ gr11 ],[ br11 ],
            [ rr12 ],[ gr12 ],[ br12 ],
            [ rr13 ],[ gr13 ],[ br13 ],
            [ rr14 ],[ gr14 ],[ br14 ],
            [ rr15 ],[ gr15 ],[ br15 ],
            [ rr16 ],[ gr16 ],[ br16 ],
            [ rr17 ],[ gr17 ],[ br17 ],
            [ rr18 ],[ gr18 ],[ br18 ],
            [ rr19 ],[ gr19 ],[ br19 ],
            [ rr20 ],[ gr20 ],[ br20 ],
            [ rr21 ],[ gr21 ],[ br21 ],
            [ rr22 ],[ gr22 ],[ br22 ],
            [ rr23 ],[ gr23 ],[ br23 ]]
        
        #Se crean ventanas de 50x50 píxeles en cada color
        #region = warped[ymin:ymax, xmin:xmax]
        region0 = warped[30:80, 30:80]
        region1 = warped[30:80, 170:220]    
        region2 = warped[30:80, 310:360]
        region3 = warped[30:80, 450:500]    
        region4 = warped[30:80, 590:640]
        region5 = warped[30:80, 730:780]
        region6 = warped[170:220, 30:80]
        region7 = warped[170:220, 170:220]
        region8 = warped[170:220, 310:360]
        region9 = warped[170:220, 450:500]
        region10 = warped[170:220, 590:640]
        region11 = warped[170:220, 730:780]
        region12 = warped[310:360, 30:80]
        region13 = warped[310:360, 170:220]
        region14 = warped[310:360, 310:360]
        region15 = warped[310:360, 450:500]
        region16 = warped[310:360, 590:640]
        region17 = warped[310:360, 730:780]
        region18 = warped[450:500, 30:80]
        region19 = warped[450:500, 170:220]
        region20 = warped[450:500, 310:360]
        region21 = warped[450:500, 450:500]
        region22 = warped[450:500, 590:640]
        region23 = warped[450:500, 730:780]
        
    #Se obtiene el promedio en cada color de las ventanas anteriores
        b0, g0, r0 = np.mean(region0, axis=(0,1))  
        b1, g1, r1 = np.mean(region1, axis=(0,1))    
        b2, g2, r2 = np.mean(region2, axis=(0,1))
        b3, g3, r3 = np.mean(region3, axis=(0,1))
        b4, g4, r4 = np.mean(region4, axis=(0,1))    
        b5, g5, r5 = np.mean(region5, axis=(0,1))    
        b6, g6, r6 = np.mean(region6, axis=(0,1))    
        b7, g7, r7 = np.mean(region7, axis=(0,1))    
        b8, g8, r8 = np.mean(region8, axis=(0,1))    
        b9, g9, r9 = np.mean(region9, axis=(0,1))    
        b10, g10, r10 = np.mean(region10, axis=(0,1))    
        b11, g11, r11 = np.mean(region11, axis=(0,1))    
        b12, g12, r12 = np.mean(region12, axis=(0,1))    
        b13, g13, r13 = np.mean(region13, axis=(0,1))    
        b14, g14, r14 = np.mean(region14, axis=(0,1))    
        b15, g15, r15 = np.mean(region15, axis=(0,1))    
        b16, g16, r16 = np.mean(region16, axis=(0,1))    
        b17, g17, r17 = np.mean(region17, axis=(0,1))    
        b18, g18, r18 = np.mean(region18, axis=(0,1))    
        b19, g19, r19 = np.mean(region19, axis=(0,1))    
        b20, g20, r20 = np.mean(region20, axis=(0,1))
        b21, g21, r21 = np.mean(region21, axis=(0,1))
        b22, g22, r22 = np.mean(region22, axis=(0,1))    
        b23, g23, r23 = np.mean(region23, axis=(0,1))
        
        #Se crea la matrix A con el promedio de cada color
        Amean =[[ r0,g0,b0,0,0,0,0,0,0 ],
                [ 0,0,0,r0,g0,b0,0,0,0 ],
                [ 0,0,0,0,0,0,r0,g0,b0 ],        
                [ r1,g1,b1,0,0,0,0,0,0 ],
                [ 0,0,0,r1,g1,b1,0,0,0 ],
                [ 0,0,0,0,0,0,r1,g1,b1 ],            
                [ r2,g2,b2,0,0,0,0,0,0 ],
                [ 0,0,0,r2,g2,b2,0,0,0 ],
                [ 0,0,0,0,0,0,r2,g2,b2 ],        
                [ r3,g3,b3,0,0,0,0,0,0 ],
                [ 0,0,0,r3,g3,b3,0,0,0 ],
                [ 0,0,0,0,0,0,r3,g3,b3 ],        
                [ r4,g4,b4,0,0,0,0,0,0 ],
                [ 0,0,0,r4,g4,b4,0,0,0 ],
                [ 0,0,0,0,0,0,r4,g4,b4 ],        
                [ r5,g5,b5,0,0,0,0,0,0 ],
                [ 0,0,0,r5,g5,b5,0,0,0 ],
                [ 0,0,0,0,0,0,r5,g5,b5 ],        
                [ r6,g6,b6,0,0,0,0,0,0 ],
                [ 0,0,0,r6,g6,b6,0,0,0 ],
                [ 0,0,0,0,0,0,r6,g6,b6 ],        
                [ r7,g7,b7,0,0,0,0,0,0 ],
                [ 0,0,0,r7,g7,b7,0,0,0 ],
                [ 0,0,0,0,0,0,r7,g7,b7 ],        
                [ r8,g8,b8,0,0,0,0,0,0 ],
                [ 0,0,0,r8,g8,b8,0,0,0 ],
                [ 0,0,0,0,0,0,r8,g8,b8 ],        
                [ r9,g9,b9,0,0,0,0,0,0 ],
                [ 0,0,0,r9,g9,b9,0,0,0 ],
                [ 0,0,0,0,0,0,r9,g9,b9 ],        
                [ r10,g10,b10,0,0,0,0,0,0 ],
                [ 0,0,0,r10,g10,b10,0,0,0 ],
                [ 0,0,0,0,0,0,r10,g10,b10 ],        
                [ r11,g11,b11,0,0,0,0,0,0 ],
                [ 0,0,0,r11,g11,b11,0,0,0 ],
                [ 0,0,0,0,0,0,r11,g11,b11 ],        
                [ r12,g12,b12,0,0,0,0,0,0 ],
                [ 0,0,0,r12,g12,b12,0,0,0 ],
                [ 0,0,0,0,0,0,r12,g12,b12 ],        
                [ r13,g13,b13,0,0,0,0,0,0 ],
                [ 0,0,0,r13,g13,b13,0,0,0 ],
                [ 0,0,0,0,0,0,r13,g13,b13 ],        
                [ r14,g14,b14,0,0,0,0,0,0 ],
                [ 0,0,0,r14,g14,b14,0,0,0 ],
                [ 0,0,0,0,0,0,r14,g14,b14 ],        
                [ r15,g15,b15,0,0,0,0,0,0 ],
                [ 0,0,0,r15,g15,b15,0,0,0 ],
                [ 0,0,0,0,0,0,r15,g15,b15 ],        
                [ r16,g16,b16,0,0,0,0,0,0 ],
                [ 0,0,0,r16,g16,b16,0,0,0 ],
                [ 0,0,0,0,0,0,r16,g16,b16 ],            
                [ r17,g17,b17,0,0,0,0,0,0 ],
                [ 0,0,0,r17,g17,b17,0,0,0 ],
                [ 0,0,0,0,0,0,r17,g17,b17 ],        
                [ r18,g18,b18,0,0,0,0,0,0 ],
                [ 0,0,0,r18,g18,b18,0,0,0 ],
                [ 0,0,0,0,0,0,r18,g18,b18 ],        
                [ r19,g19,b19,0,0,0,0,0,0 ],
                [ 0,0,0,r19,g19,b19,0,0,0 ],
                [ 0,0,0,0,0,0,r19,g19,b19 ],        
                [ r20,g20,b20,0,0,0,0,0,0 ],
                [ 0,0,0,r20,g20,b20,0,0,0 ],
                [ 0,0,0,0,0,0,r20,g20,b20 ],        
                [ r21,g21,b21,0,0,0,0,0,0 ],
                [ 0,0,0,r21,g21,b21,0,0,0 ],
                [ 0,0,0,0,0,0,r21,g21,b21 ],        
                [ r22,g22,b22,0,0,0,0,0,0 ],
                [ 0,0,0,r22,g22,b22,0,0,0 ],
                [ 0,0,0,0,0,0,r22,g22,b22 ],             
                [ r23,g23,b23,0,0,0,0,0,0 ],
                [ 0,0,0,r23,g23,b23,0,0,0 ],
                [ 0,0,0,0,0,0,r23,g23,b23 ]]
            
        #Se obtiene x
        #x=(((A^T)A)^⁻1)(A^T)(b)
    
        x = np.matmul(np.matmul(np.linalg.inv(np.matmul(np.transpose(Amean),Amean)),np.transpose(Amean)),b)
        
        #La matriz de calibración es
        self.alphasmean = (x[0,0],x[1,0],x[2,0],0,
                      x[3,0],x[4,0],x[5,0],0,
                      x[6,0],x[7,0],x[8,0],0)
        
        
    # Guarda la matriz de calibración para ser utilizada posteriormente con cualquier imagen
        arr=np.array([self.alphasmean])
        np.savetxt(self.matrix,arr,delimiter=',',fmt='%f')
        
        # Abre la imagen transformada
        ck = Image.open(self.warpedout) 
        
        # Multiplica una imagen por una matriz
    # Basado en: https://stackoverflow.com/questions/10885984/multiply-each-pixel-in-an-image-by-a-factor
        # Multiplica pixel a pixel para obtener vref
        ck = ck.convert('RGB', self.alphasmean) 
        ck.save(self.checkerout)
        changemean = cv2.imread(self.checkerout)
        cv2.imshow("Changemean", changemean)
        
        #Para la distancia euclidea del promedio por cada color
        
        #Se crean ventanas de 50x50 píxeles en cada color
        #region0 = changemean[ymin:ymax, xmin:xmax]
        regionc0 = changemean[30:80, 30:80]
        regionc1 = changemean[30:80, 170:220]    
        regionc2 = changemean[30:80, 310:360]
        regionc3 = changemean[30:80, 450:500]    
        regionc4 = changemean[30:80, 590:640]
        regionc5 = changemean[30:80, 730:780]
        regionc6 = changemean[170:220, 30:80]
        regionc7 = changemean[170:220, 170:220]
        regionc8 = changemean[170:220, 310:360]
        regionc9 = changemean[170:220, 450:500]
        regionc10 = changemean[170:220, 590:640]
        regionc11 = changemean[170:220, 730:780]
        regionc12 = changemean[310:360, 30:80]
        regionc13 = changemean[310:360, 170:220]
        regionc14 = changemean[310:360, 310:360]
        regionc15 = changemean[310:360, 450:500]
        regionc16 = changemean[310:360, 590:640]
        regionc17 = changemean[310:360, 730:780]
        regionc18 = changemean[450:500, 30:80]
        regionc19 = changemean[450:500, 170:220]
        regionc20 = changemean[450:500, 310:360]
        regionc21 = changemean[450:500, 450:500]
        regionc22 = changemean[450:500, 590:640]
        regionc23 = changemean[450:500, 730:780]

    #Se obtiene el promedio en cada color de las ventanas anteriores        
        bc0, gc0, rc0 = np.mean(regionc0, axis=(0,1))
        bc1, gc1, rc1 = np.mean(regionc1, axis=(0,1))
        bc2, gc2, rc2 = np.mean(regionc2, axis=(0,1))
        bc3, gc3, rc3 = np.mean(regionc3, axis=(0,1))
        bc4, gc4, rc4 = np.mean(regionc4, axis=(0,1))
        bc5, gc5, rc5 = np.mean(regionc5, axis=(0,1))
        bc6, gc6, rc6 = np.mean(regionc6, axis=(0,1))
        bc7, gc7, rc7 = np.mean(regionc7, axis=(0,1))
        bc8, gc8, rc8 = np.mean(regionc8, axis=(0,1))
        bc9, gc9, rc9 = np.mean(regionc9, axis=(0,1))
        bc10, gc10, rc10 = np.mean(regionc10, axis=(0,1))
        bc11, gc11, rc11 = np.mean(regionc11, axis=(0,1))
        bc12, gc12, rc12 = np.mean(regionc12, axis=(0,1))
        bc13, gc13, rc13 = np.mean(regionc13, axis=(0,1))
        bc14, gc14, rc14 = np.mean(regionc14, axis=(0,1))
        bc15, gc15, rc15 = np.mean(regionc15, axis=(0,1))
        bc16, gc16, rc16 = np.mean(regionc16, axis=(0,1))
        bc17, gc17, rc17 = np.mean(regionc17, axis=(0,1))
        bc18, gc18, rc18 = np.mean(regionc18, axis=(0,1))
        bc19, gc19, rc19 = np.mean(regionc19, axis=(0,1))
        bc20, gc20, rc20 = np.mean(regionc20, axis=(0,1))
        bc21, gc21, rc21 = np.mean(regionc21, axis=(0,1))
        bc22, gc22, rc22 = np.mean(regionc22, axis=(0,1))
        bc23, gc23, rc23 = np.mean(regionc23, axis=(0,1))
        
        #Distancia euclidea: https://en.wikipedia.org/wiki/Color_difference
        #Distancia euclidea Valores de referencia vs valores de imagen original
        de0=np.sqrt(np.power(rr0-r0,2)+np.power(gr0-g0,2)+np.power(br0-b0,2))
        de1=np.sqrt(np.power(rr1-r1,2)+np.power(gr1-g1,2)+np.power(br1-b1,2))
        de2=np.sqrt(np.power(rr2-r2,2)+np.power(gr2-g2,2)+np.power(br2-b2,2))
        de3=np.sqrt(np.power(rr3-r3,2)+np.power(gr3-g3,2)+np.power(br3-b3,2))
        de4=np.sqrt(np.power(rr4-r4,2)+np.power(gr4-g4,2)+np.power(br4-b4,2))
        de5=np.sqrt(np.power(rr5-r5,2)+np.power(gr5-g5,2)+np.power(br5-b5,2))
        de6=np.sqrt(np.power(rr6-r6,2)+np.power(gr6-g6,2)+np.power(br6-b6,2))
        de7=np.sqrt(np.power(rr7-r7,2)+np.power(gr7-g7,2)+np.power(br7-b7,2))
        de8=np.sqrt(np.power(rr8-r8,2)+np.power(gr8-g8,2)+np.power(br8-b8,2))
        de9=np.sqrt(np.power(rr9-r9,2)+np.power(gr9-g9,2)+np.power(br9-b9,2))
        de10=np.sqrt(np.power(rr10-r10,2)+np.power(gr10-g10,2)+np.power(br10-b10,2))
        de11=np.sqrt(np.power(rr11-r11,2)+np.power(gr11-g11,2)+np.power(br11-b11,2))
        de12=np.sqrt(np.power(rr12-r12,2)+np.power(gr12-g12,2)+np.power(br12-b12,2))
        de13=np.sqrt(np.power(rr13-r13,2)+np.power(gr13-g13,2)+np.power(br13-b13,2))
        de14=np.sqrt(np.power(rr14-r14,2)+np.power(gr14-g14,2)+np.power(br14-b14,2))
        de15=np.sqrt(np.power(rr15-r15,2)+np.power(gr15-g15,2)+np.power(br15-b15,2))
        de16=np.sqrt(np.power(rr16-r16,2)+np.power(gr16-g16,2)+np.power(br16-b16,2))
        de17=np.sqrt(np.power(rr17-r17,2)+np.power(gr17-g17,2)+np.power(br17-b17,2))
        de18=np.sqrt(np.power(rr18-r18,2)+np.power(gr18-g18,2)+np.power(br18-b18,2))
        de19=np.sqrt(np.power(rr19-r19,2)+np.power(gr19-g19,2)+np.power(br19-b19,2))
        de20=np.sqrt(np.power(rr20-r20,2)+np.power(gr20-g20,2)+np.power(br20-b20,2))
        de21=np.sqrt(np.power(rr21-r21,2)+np.power(gr21-g21,2)+np.power(br21-b21,2))
        de22=np.sqrt(np.power(rr22-r22,2)+np.power(gr22-g22,2)+np.power(br22-b22,2))
        de23=np.sqrt(np.power(rr23-r23,2)+np.power(gr23-g23,2)+np.power(br23-b23,2))

        #Distancia euclidea valores de referencia vs valores de imagen calibrada
        dec0=np.sqrt(np.power(rr0-rc0,2)+np.power(gr0-gc0,2)+np.power(br0-bc0,2))
        dec1=np.sqrt(np.power(rr1-rc1,2)+np.power(gr1-gc1,2)+np.power(br1-bc1,2))
        dec2=np.sqrt(np.power(rr2-rc2,2)+np.power(gr2-gc2,2)+np.power(br2-bc2,2))
        dec3=np.sqrt(np.power(rr3-rc3,2)+np.power(gr3-gc3,2)+np.power(br3-bc3,2))
        dec4=np.sqrt(np.power(rr4-rc4,2)+np.power(gr4-gc4,2)+np.power(br4-bc4,2))
        dec5=np.sqrt(np.power(rr5-rc5,2)+np.power(gr5-gc5,2)+np.power(br5-bc5,2))
        dec6=np.sqrt(np.power(rr6-rc6,2)+np.power(gr6-gc6,2)+np.power(br6-bc6,2))
        dec7=np.sqrt(np.power(rr7-rc7,2)+np.power(gr7-gc7,2)+np.power(br7-bc7,2))
        dec8=np.sqrt(np.power(rr8-rc8,2)+np.power(gr8-gc8,2)+np.power(br8-bc8,2))
        dec9=np.sqrt(np.power(rr9-rc9,2)+np.power(gr9-gc9,2)+np.power(br9-bc9,2))
        dec10=np.sqrt(np.power(rr10-rc10,2)+np.power(gr10-gc10,2)+np.power(br10-bc10,2))
        dec11=np.sqrt(np.power(rr11-rc11,2)+np.power(gr11-gc11,2)+np.power(br11-bc11,2))
        dec12=np.sqrt(np.power(rr12-rc12,2)+np.power(gr12-gc12,2)+np.power(br12-bc12,2))
        dec13=np.sqrt(np.power(rr13-rc13,2)+np.power(gr13-gc13,2)+np.power(br13-bc13,2))
        dec14=np.sqrt(np.power(rr14-rc14,2)+np.power(gr14-gc14,2)+np.power(br14-bc14,2))
        dec15=np.sqrt(np.power(rr15-rc15,2)+np.power(gr15-gc15,2)+np.power(br15-bc15,2))
        dec16=np.sqrt(np.power(rr16-rc16,2)+np.power(gr16-gc16,2)+np.power(br16-bc16,2))
        dec17=np.sqrt(np.power(rr17-rc17,2)+np.power(gr17-gc17,2)+np.power(br17-bc17,2))
        dec18=np.sqrt(np.power(rr18-rc18,2)+np.power(gr18-gc18,2)+np.power(br18-bc18,2))
        dec19=np.sqrt(np.power(rr19-rc19,2)+np.power(gr19-gc19,2)+np.power(br19-bc19,2))
        dec20=np.sqrt(np.power(rr20-rc20,2)+np.power(gr20-gc20,2)+np.power(br20-bc20,2))
        dec21=np.sqrt(np.power(rr21-rc21,2)+np.power(gr21-gc21,2)+np.power(br21-bc21,2))
        dec22=np.sqrt(np.power(rr22-rc22,2)+np.power(gr22-gc22,2)+np.power(br22-bc22,2))
        dec23=np.sqrt(np.power(rr23-rc23,2)+np.power(gr23-gc23,2)+np.power(br23-bc23,2))
 
        # Crea Boxplot de distancias euclideas: https://matplotlib.org/3.1.0/tutorials/introductory/pyplot.html
        names = ['DarkSkin','LightSkin','BLueSKy','Foliage','BlueFlower','BLuishGreen','Orange','PurplishBlue','ModerateRed','Purple','YelloweGreen','OrangeYellow','Blue','Green','Red','Yellow','Magenta','Cyan','White(.05*)','neutral8(.23*)','neutral6.5(.44*)','neutral5(.70*,)','neutral3.5(1.05*)','black(1.50*)']
        de=[de0,de1,de2,de3,de4,de5,de6,de7,de8,de9,de10,de11,de12,de13,de14,de15,de16,de17,de18,de19,de20,de21,de22,de23]
        dec=[dec0,dec1,dec2,dec3,dec4,dec5,dec6,dec7,dec8,dec9,dec10,dec11,dec12,dec13,dec14,dec15,dec16,dec17,dec18,dec19,dec20,dec21,dec22,dec23]

        plt.figure(figsize=(10,4))
        
        ax = plt.subplot(111)
        ax.set_xticklabels(names, rotation = 90)
        
        ax.plot(names,de,'ro', label='RealV vs Image')
        ax.plot(names,dec,'g*', label='RealV vs ImCalibrated')
        plt.title('Distancia Euclidea')
        
        chartBox = ax.get_position()
        ax.set_position([chartBox.x0, chartBox.y0, chartBox.width*0.8, chartBox.height])
        ax.legend(loc='upper left', bbox_to_anchor=(1, 0.8), shadow=True, ncol=1)
        plt.savefig(self.de)
        plt.show()
        
        box_plot_data=[de,dec]
        plt.boxplot(box_plot_data,patch_artist=True,labels=['DE: RealV vs Image','DE: RealV vs ImCalibrated'])
        plt.title('Boxplot Distancia euclidea')
        plt.savefig(self.dechg)
        plt.show()
        
        plt.close()

        print('Presione cualquier tecla para terminar')  
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
    def imageCalibration(self):
        #Abre la imagen para calibrar
        im = Image.open(self.image)
        
        # Multiplica una imagen por una matriz
        # Basado en: https://stackoverflow.com/questions/10885984/multiply-each-pixel-in-an-image-by-a-factor
        # Multiplica pixel a pixel para obtener vref
                
        mat=np.loadtxt(self.matriximg,delimiter=',')        
        mat=(mat[0],mat[1],mat[2],0,mat[4],mat[5],mat[6],0,mat[8],mat[9],mat[10],0)
        
        im = im.convert('RGB', mat) 
        im.save(self.imageout)
        
        imageout = cv2.imread(self.imageout)
        imagein=cv2.imread(self.image)
    
        # Hace más pequeña la imagen para poder observarla en pantalla
        height, width = imageout.shape[:2]
        imagein = cv2.resize(imagein,(int(self.scalefactor2*width), int(self.scalefactor2*height)), interpolation = cv2.INTER_NEAREST)
        imageout = cv2.resize(imageout,(int(self.scalefactor2*width), int(self.scalefactor2*height)), interpolation = cv2.INTER_NEAREST)
        
        cv2.imshow("Image Input", imagein)
        cv2.imshow("Image Output", imageout)

        print('Presione cualquier tecla para terminar')        
        
        cv2.waitKey(0)
        cv2.destroyAllWindows()
