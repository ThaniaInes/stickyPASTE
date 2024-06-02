import cv2
import numpy as np


class ImageProcessor:

    def __init__(self):
        self.letra_img = None
        # self.img_a_convertir = None

    def es_victima(self):
        
        # self.img = cv2.imread(self.img)
        gris = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gris, 120, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contorno_img = np.copy(self.img)
        for cont in contours:
            cv2.drawContours(contorno_img, [cont], -1, (0, 255, 0), 2)
        return contours if len(contours) == 1 and len(contours[0]) <= 10 else None

    def devolver_letra_victimas(self):
        salida = None
        gris = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gris, 120, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        thresh_img = np.copy(thresh)
        for cont in contours:
            cv2.drawContours(thresh_img, [cont], -1, (0, 255, 0), 2)
        if len(contours) == 1 and len(contours[0]) <= 10:
            approx = cv2.minAreaRect(contours[0])
            angulo = approx[2]
            if angulo % 90 == 0:
                x = int(approx[0][0])
                y = int(approx[0][1])
                mitad_ancho = int(approx[1][0] / 2)
                mitad_alto = int(approx[1][1] / 2)
                cuadritoArriba = thresh[y - mitad_alto:y - int(mitad_alto / 3), x - int(mitad_ancho / 3):x + int(mitad_ancho / 3)]
                cuadritoAbajo = thresh[y + int(mitad_alto / 3):y + mitad_alto, x - int(mitad_ancho / 3):x + int(mitad_ancho / 3)]
                pixeles_negros_arriba = np.count_nonzero(cuadritoArriba == 0)
                pixeles_negros_abajo = np.count_nonzero(cuadritoAbajo == 0)
                if pixeles_negros_abajo <= 5 and pixeles_negros_arriba <= 5:
                    salida = 'H'
                    return salida
                elif pixeles_negros_abajo >= 13 and pixeles_negros_arriba >= 13:
                    salida = 'S'
                    return salida
                elif pixeles_negros_abajo >= 15 and pixeles_negros_arriba <= 5:
                    salida = 'U'
                    return salida
                return salida
        return salida

    def reconocer_limpiar_cartel(self):
        salida = None
        gris=cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        _, thresh=cv2.threshold(gris, 120, 255, cv2.THRESH_BINARY)
        contours,_ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        approx=cv2.minAreaRect(contours[0])
        angulo=approx[2]
        if abs(angulo)==45:
            alto, ancho=thresh.shape[0], thresh.shape[1]
            M=cv2.getRotationMatrix2D((ancho/2,alto/2),angulo,1)
            thresh_rot=cv2.warpAffine(thresh,M,(ancho,alto))
            imagen_rot=cv2.warpAffine(self.img,M,(ancho,alto))
            contours,_ = cv2.findContours(thresh_rot, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            approx=cv2.minAreaRect(contours[0])
            x=int(approx[0][0])
            y=int(approx[0][1])
            mitad_ancho=int(approx[1][0]/2)
            mitad_alto=int(approx[1][1]/2)
            rect=imagen_rot[y-mitad_alto:y+mitad_alto, x-mitad_ancho:x+mitad_ancho]
            return rect, True
        return salida   

    def devolver_letra_carteles(self):
        salida = None
        gris = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gris, 120, 255, cv2.THRESH_BINARY)
        contornos, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if len(contornos) == 0:
            return None
        approx = cv2.minAreaRect(contornos[0])
        angulo = approx[2]
        if abs(angulo) == 45:
            alto, ancho = thresh.shape[0], thresh.shape[1]
            M = cv2.getRotationMatrix2D((ancho / 2, alto / 2), angulo, 1)
            thresh_rot = cv2.warpAffine(thresh, M, (ancho, alto))
            imagen_rot = cv2.warpAffine(self.img, M, (ancho, alto))
            contornos, _ = cv2.findContours(thresh_rot, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            if len(contornos) == 0:
                return None
            approx = cv2.minAreaRect(contornos[0])
            x = int(approx[0][0])
            y = int(approx[0][1])
            mitadAncho = int(approx[1][0] / 2)
            mitadAlto = int(approx[1][1] / 2)
            if y - mitadAlto < 0 or y + mitadAlto > imagen_rot.shape[0] or x - mitadAncho < 0 or x + mitadAncho > imagen_rot.shape[1]:
                return None
            rect = imagen_rot[y - mitadAlto:y + mitadAlto, x - mitadAncho:x + mitadAncho]
            amarillo, rojo, negro, blanco = 0, 0, 0, 0
            for x in range(rect.shape[0]):
                for y in range(rect.shape[1]):
                    b, g, r = rect[x, y]
                    if b > 200 and g > 200 and r > 200:
                        blanco += 1
                    elif b <= 1 and g <= 1 and r <= 1:
                        negro += 1
                    elif b > 70 and g < 5 and r > 190:
                        rojo += 1
                    elif b < 10 and g > 190 and r > 195:
                        amarillo += 1
            if (rojo + blanco) > (negro + amarillo) and rojo > blanco and blanco > negro:
                return salida == 'F'
            elif (blanco + negro) > (amarillo + rojo) and blanco > negro:
                return salida == 'P'
            elif (blanco + negro) > (amarillo + rojo):
                return salida == 'C'
            elif (rojo + amarillo) > (negro + blanco):
                return salida == 'O'
            return salida
        return salida

# Nuevo argumento
    def procesar(self, resultado):
        self.img = resultado
        if self.es_victima() is not None:
            self.letra_img = self.devolver_letra_victimas()
            return self.letra_img 
        else:
            resultado = self.reconocer_limpiar_cartel()
            if resultado is not None:
                self.letra_img == self.devolver_letra_carteles()  
                return self.letra_img
            return self.letra_img