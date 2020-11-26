    # -*- coding: utf-8 -*-
def funcionColor():
    
    import cv2
    import numpy as np
    import time
    from nms_fast import mincuadro
        
    cap = cv2.VideoCapture(0)
    m=25
    m1=500

    cap.set(3,320)
    cap.set(4,240)
    
#    noRegions = len(regions)
    
    def colorChange(frame):
    #convertimos a escalas de grises
        H = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) #Convertirlo a espacio de color HSV
        return H
    
    def overlapRectangles(reg,rect):
          if(reg[2]<rect[0] or rect[2]<reg[0] or reg[3]<rect[1] or rect[3]<reg[1]):
              return False
          else:
              return True
    
    
    def colorFilter(frame):
    #Los valores maximo y minimo de H,S y V se guardan en funcion de la posicion de los sliders
##        hMin = cv2.getTrackbarPos('H Minimo','image')
##        hMax = cv2.getTrackbarPos('H Maximo','image')
##        sMin = cv2.getTrackbarPos('S Minimo','image')
##        sMax = cv2.getTrackbarPos('S Maximo','image')
##        vMin = cv2.getTrackbarPos('V Minimo','image')
##        vMax = cv2.getTrackbarPos('V Maximo','image')
        
## para Pruebas con color verde
        hMin = 30
        hMax = 90
        sMin = 120 
        sMax = 250
        vMin = 95
        vMax = 200
     
    #Se crea un array con las posiciones minimas y maximas
        lower=np.array([hMin,sMin,vMin])
        upper=np.array([hMax,sMax,vMax])
     
    #Deteccion de colores
        mask = cv2.inRange(frame, lower, upper)
        return mask, lower, upper
    
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
      #print(type(frame))
      frame2 = np.copy (frame)
      gris = colorChange(frame)
      [gris,lower,upper] = colorFilter(gris)
      
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
      
    # Buscamos contorno en la imagen OJO
      try:
          im,contornos, hierarchy = cv2.findContours(contornosimg,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
      except:
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
      
      # Define si hay movimiento dentro de las regiones FIXED FOR 3 REGIONS
            
#      for rect in cajas:
#          countReg = 1
#          for reg in regions:
#              overlap = overlapRectangles(reg,rect)
#              if overlap:
#                  print "Hay movimiento en la region ", countReg
#              countReg+=1
#              
#      for rects in range (0,noRegions):
#                cv2.rectangle(image2, (regions[rects][0], regions[rects][1]), (regions[rects][2], regions[rects][3]), (255, 0, 255), 2) # Con las coordenadas construye el rectángulo
#   
      
      #Mostrar los resultados y salir
      
      #cv2.imshow('camara',frame)
      #cv2.imshow('gris',gris)
      #cv2.imshow("Umbral", umbral)
      #cv2.imshow("Resta", resta)
      #cv2.imshow("Contorno", contornosimg)
      cv2.imshow("other", image2)
      
      
      #tiempo de espera para que se vea bien

      k=cv2.waitKey(5) & 0xFF
      time.sleep(0.015)
      if k == 27:
          break
      
    cap.release()
    cv2.destroyAllWindows()
    for i in range (1,10):
        cv2.waitKey(1)
  
    return lower, upper
    #return upper, lower
