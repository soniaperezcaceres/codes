    # -*- coding: utf-8 -*-
def funcionMovimientoEnRegion(regionCoordinates,tiempo,noRegion,lowerValue,upperValue):
    
    import cv2
    import numpy as np
    import time
    from nms_fast import mincuadro
     
    cap = cv2.VideoCapture(0)
    m=25
    m1=500
    chrono = 0
    
    def colorChange(frame):
    #convertimos a escalas de grises
        H = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) #Convertirlo a espacio de color HSV
        return H
    
    def overlapRectangles(reg,rect):
          if(reg[2]<rect[0] or rect[2]<reg[0] or reg[3]<rect[1] or rect[3]<reg[1]):
              return False
          else:
              return True
          
    def currentTime(): # Obtain current time in seconds
        time1 = time.localtime()  
        time2 = (time1[0],time1[1],time1[2],time1[3],time1[4],time1[5],time1[6],time1[7],time1[8])
        currentTime = time.mktime(time2)
        return currentTime
    
    def colorFilter(frame):
    #Se crea un array con las posiciones minimas y maximas
        lower=lowerValue
        upper=upperValue
    #Deteccion de colores
        mask = cv2.inRange(frame, lower, upper)
        return mask
    
    #nos servira para obterner el fondo
    fondo = None
    
    #recorremos todos los frames
    while(1):
      _,frame = cap.read() #Leer un frame
      #print(type(frame))
      frame2 = np.copy (frame)
      gris = colorChange(frame)
      gris = colorFilter(gris)
     
      
    #aplicamos suavizado para eliminar el ruido
      gris = cv2.GaussianBlur(gris, (21, 21), 0)
      
      
    #si todavia no hemos obtenido el fondo, lo obtenemos
      if fondo is None:
          fondoanterior = gris
          fondo = gris
          continue
      else:
          fondo = fondoanterior
      
      
    #calculo la dif etre el fondo y el frame
      resta = cv2.absdiff(fondo, gris)
     
    # Aplicamos un umbral
      umbral = cv2.threshold(resta, m, 255, cv2.THRESH_BINARY)[1]
     
    # Dilatamos el umbral para tapar agujeros
      umbral = cv2.dilate(umbral, None, iterations=2)
     
    # Copiamos el umbral para detectar los contornos
      contornosimg = umbral.copy()
      
    # Buscamos contorno en la imagen
      contornos, hierarchy = cv2.findContours(contornosimg,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
      cajas = []
    # Recorremos todos los contornos encontrados
      for c in contornos:
    # Eliminamos los contornos mas pequenos
           if cv2.contourArea(c) < m1:
              continue    
    # Obtenemos el bounds del contorno, el rectangulo mayor que engloba al contorno
           (x, y, w, h) = cv2.boundingRect(c)
    # Dibujamos el rectangulo del bounds
           cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
           cajas.append((x,y,x+w,y+h))
      
      image2 = mincuadro(frame2,np.array(cajas)) 
      print cajas
      # Define si hay movimiento dentro de las regiones FIXED FOR 3 REGIONS
            
      for rect in cajas:
          overlap = overlapRectangles(regionCoordinates,rect)
          if overlap:
              if chrono == 0:
                  chrono = currentTime()
                  print "Hay movimiento en la region ", noRegion
              else:
                  chrono2 = currentTime()
                  if (chrono2 - chrono) >= tiempo:
                      cap.release()
                      cv2.destroyAllWindows()
                      return True
                      break
                  
          else:
              if chrono == 0:
                  pass
              else:
                  print('Se saltó un paso, recomience')
                  chrono = 0
                  
             
      cv2.rectangle(image2, (regionCoordinates[0], regionCoordinates[1]), (regionCoordinates[2], regionCoordinates[3]), (255, 0, 255), 2) # Con las coordenadas construye el rectángulo
   
      #Mostrar los resultados y salir
      
      cv2.imshow('camara',frame)
      cv2.imshow('gris',gris)
      cv2.imshow("Umbral", umbral)
      cv2.imshow("Resta", resta)
      cv2.imshow("Contorno", contornosimg)
      cv2.imshow("other", image2)
      fondoanterior = gris

      k = cv2.waitKey(5) & 0xFF
  
  #tiempo de espera para que se vea bien
      time.sleep(0.015)
    
  #si ha pulsado escape para salir, salimos
      if k == 27:
    #liberamos la camara y cerramos todas las ventanas
        cap.release()
        cv2.destroyAllWindows()
    
