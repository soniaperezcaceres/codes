   # -*- coding: utf-8 -*-
def newUser(numFrames,lower,upper):
    
    import cv2
    import numpy as np
    import time
    from nms_fast import mincuadro

        

#################################################### Definir Funciones
 ###### Funciones para Bounding Boxes
    
    def colorChange(frame):
    #convertimos a escalas de grises
        H = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) #Convertirlo a espacio de color HSV
        return H
    
    def colorFilter(frameHSV,lower,upper):
    #Deteccion de colores
        mask = cv2.inRange(frameHSV,lower,upper)
        return mask
    
##    def nothing(x):
##       pass

    def currentTime(): # Obtain current time in seconds
        time1 = time.localtime()  
        time2 = (time1[0],time1[1],time1[2],time1[3],time1[4],time1[5],time1[6],time1[7],time1[8])
        currentTime = time.mktime(time2)
        return currentTime

## Ejemplo de cómo usar timer
##    chrono = currentTime()
##    chrono_aux = currentTime()
##    if (chrono_aux - chrono) >= tiempo:

    frameVar = 1
    
#################################################### Optical FLow parameters
    cap = cv2.VideoCapture(0)
    m=25
    m1=500

    cap.set(3,320)
    cap.set(4,240)
    
    fgbg = cv2.bgsegm.createBackgroundSubtractorMOG()
    fondoAnteriorOF = None
    fondoAnteriorBB = None

    ret, frame1 = cap.read()
    prvs = cv2.cvtColor(frame1,cv2.COLOR_BGR2GRAY)
    hsv = np.zeros_like(frame1)
    #Acá puedo cambiar los 255 por menos, de pronto así hay menos colores y el video se pone más rápido
    hsv[...,1] = 5

#################################################### Initialize parameters that will be returned at the end of the function
# N = NO / p = piel / S = SÍ / m = movimeinto
    SpSm = 0 
    topMovementCounter = 2
    

########################################################## WHILE Loop
    while(SpSm < topMovementCounter):
        


      if (SpSm >= topMovementCounter):
            return 1
            break
            cap.release()
            cv2.destroyAllWindows()
            for i in range (1,10):
                    cv2.waitKey(0)


      _,frame = cap.read() #Leer un frame
      
      if frameVar != 1:
          if frameVar == numFrames:
              frameVar = 1
##              print 'Skips'
              continue
          else:
              frameVar = frameVar +1
##              print 'Skips'
              continue
            
################### BOUNDING BOXES SETUP
##      print 'Processes'
      frame2 = frame
      frameHSV = colorChange(frame2)
      grisBB = colorFilter(frameHSV,lower,upper)
      grisBB = cv2.GaussianBlur(grisBB, (21, 21), 0) #aplicamos suavizado para eliminar el ruido


######################################################## FILTRO DE FONDOS
      if fondoAnteriorBB is None:
          fondoAnteriorBB = grisBB
          continue
      
      if fondoAnteriorOF is None:
          grisOF = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
          fondoAnteriorOF = grisOF
          continue

################### OPTICAL FLOW SETUP
      frameOF = frame
      grisOF = cv2.cvtColor(frameOF,cv2.COLOR_BGR2GRAY)


#### OPTICAL FLOW PROCESSING
      vfield = np.zeros_like(frameOF)

      restaOF = cv2.absdiff(fondoAnteriorOF, grisOF)
      ret,thresh = cv2.threshold(restaOF,127,255,0)
      im,contours,hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
      cv2.drawContours(frameOF,contours, -1, (0,255,0), 3)


#### BOUNDING BOXES PROCESSING
      restaBB = cv2.absdiff(fondoAnteriorBB, grisBB)  #calculo la dif etre el fondo y el frame
      umbral = cv2.threshold(restaBB, m, 255, cv2.THRESH_BINARY)[1] # Aplicamos un umbral
      umbral = cv2.dilate(umbral, None, iterations=2)   # Dilatamos el umbral para tapar agujeros
      contornosimg = umbral.copy()  # Copiamos el umbral para detectar los contornos
      try:          # Buscamos contorno en la imagen OJO
          im,contornos, hierarchy = cv2.findContours(contornosimg,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
      except:
          contornos, hierarchy = cv2.findContours(contornosimg,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
      cajas = []
      for c in contornos:                 # Recorremos todos los contornos encontrados
           if cv2.contourArea(c) < m1:    # Eliminamos los contornos mas pequenos
              continue    

    # Obtenemos el bounds del contorno, el rectangulo mayor que engloba al contorno
           (x, y, w, h) = cv2.boundingRect(c)
    # Dibujamos el rectangulo del bounds
           cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
           cajas.append((x,y,x+w,y+h))


################### CONDICIONALES BB & OF
      if (cajas) and (contours):
          SpSm = SpSm + 1           
          print SpSm
      else:
          print 'cajas', cajas
          print 'contours', contours
          SpSm = 0
          print SpSm
          continue

      
      contours = np.vstack(contours)
      contours = np.float32(contours)
      #contours = np.asarray(contours)
      #contours = contours.astype(int)

      flow = cv2.calcOpticalFlowFarneback(fondoAnteriorOF, grisOF, None,0.4,5,7,10,7,3.5,0)
      mag, ang = cv2.cartToPolar(flow[...,0], flow[...,1])
      hsv[...,0] = ang*180/np.pi/2
      hsv[...,2] = cv2.normalize(mag,None,0,255,cv2.NORM_MINMAX)
      rgb = cv2.cvtColor(hsv,cv2.COLOR_HSV2BGR)

      
      
      image2 = mincuadro(frame2,np.array(cajas))
      cv2.imshow('frame',rgb)

      fondoAnteriorOF = grisOF

      cv2.imshow("other", image2)

      
      fondoAnteriorBB = grisBB
      frameVar = frameVar + 1
      
      #tiempo de espera para que se vea bien
    
      k=cv2.waitKey(5) & 0xFF
      time.sleep(0.015)
      if k == 27:
          break

        
    return 1 
    cap.release()
    cv2.destroyAllWindows()
    for i in range (1,10):
        cv2.waitKey(0)
