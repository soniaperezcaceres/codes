import cv2
import time
import numpy as np
 
cap = cv2.VideoCapture(1) #Puede ser VideoCapture(0) dependiendo del PC
m=25
m1=500

def colorChange(frame):
#convertimos a escalas de grises
    H = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) #Convertirlo a espacio de color HSV
    return H

def colorFilter(frame):
#Los valores maximo y minimo de H,S y V se guardan en funcion de la posicion de los sliders
    hMin = cv2.getTrackbarPos('H Minimo','image')
    hMax = cv2.getTrackbarPos('H Maximo','image')
    sMin = cv2.getTrackbarPos('S Minimo','image')
    sMax = cv2.getTrackbarPos('S Maximo','image')
    vMin = cv2.getTrackbarPos('V Minimo','image')
    vMax = cv2.getTrackbarPos('V Maximo','image')
 
#Se crea un array con las posiciones minimas y maximas
    lower=np.array([hMin,sMin,vMin])
    upper=np.array([hMax,sMax,vMax])
 
#Deteccion de colores
    mask = cv2.inRange(frame, lower, upper)
    return mask

def nothing(x):
   pass
 
#Creamos una ventana llamada 'image' en la que habra todos los sliders
cv2.namedWindow('image')
cv2.createTrackbar('H Minimo','image',0,255,nothing)
cv2.createTrackbar('H Maximo','image',0,255,nothing)
cv2.createTrackbar('S Minimo','image',0,255,nothing)
cv2.createTrackbar('S Maximo','image',0,255,nothing)
cv2.createTrackbar('V Minimo','image',0,255,nothing)
cv2.createTrackbar('V Maximo','image',0,255,nothing)
 
#nos servira para obterner el fondo
fondo = None

#recorremos todos los frames
while(1):
  _,frame = cap.read() #Leer un frame
  
  gris = colorChange(frame)
  gris = colorFilter(gris)
  
#aplicamos suavizado para eliminar el ruido
  gris = cv2.GaussianBlur(gris, (21, 21), 0)
  
#si todavia no hemos obtenido el fonod, lo obtenemos
  if fondo is None:
      fondo = gris
      continue
  
#calculo la dif etre el fondo y el frame
  resta = cv2.absdiff(fondo, gris)
 
# Aplicamos un umbral
  umbral = cv2.threshold(resta, m, 255, cv2.THRESH_BINARY)[1]
 
# Dilatamos el umbral para tapar agujeros
  umbral = cv2.dilate(umbral, None, iterations=2)
 
# Copiamos el umbral para detectar los contornos
  contornosimg = umbral.copy()
  
# Buscamos contorno en la imagen
  im, contornos, hierarchy = cv2.findContours(contornosimg,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
# Si aparece el error: ValueError: need more than 2 values to unpack, eliminar 'im' de las variables 'im, contornos, hierarchy'
 
# Recorremos todos los contornos encontrados
  for c in contornos:
# Eliminamos los contornos más pequeños
		if cv2.contourArea(c) < m1:
			continue
        
# Obtenemos el bounds del contorno, el rectángulo mayor que engloba al contorno
		(x, y, w, h) = cv2.boundingRect(c)
# Dibujamos el rectángulo del bounds
		cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

  #Mostrar los resultados y salir
  cv2.imshow('camara',frame)
  cv2.imshow('gris',gris)
  cv2.imshow("Umbral", umbral)
  cv2.imshow("Resta", resta)
  cv2.imshow("Contorno", contornosimg)
    
  k = cv2.waitKey(5) & 0xFF
  
  #tiempo de espera para que se vea bien
  
  time.sleep(0.015)
  
  #si ha pulsado escape para salir, salimos
  if k == 27:
    break

#liberamos la camara y cerramos todas las ventanas
cap.release()
cv2.destroyAllWindows()
