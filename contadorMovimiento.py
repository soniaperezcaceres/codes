    # -*- coding: utf-8 -*-
def funcionMovimientoEnRegion(regionCoordinates,tiempo,noRegion,lowerValue,upperValue):
    
    import cv2
    import numpy as np
    import time
    from nms_fast import mincuadro
    
    cap = cv2.VideoCapture(0)
    m=25
    m1=500
    cap.set(3,320)
    cap.set(4,240)
    chrono = 0
    exitHands = 0
    outHands = 0
    inHandsnoMov = 0
    prevBoxes = []
    xRange = 10
    reason = 0
    
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
        lower = lowerValue
        upper = upperValue
#        lower=[33,78,97]
#        upper=[88,163,255]
    #Deteccion de colores
        mask = cv2.inRange(frame, lower, upper)
        return mask

    def umbralMovimiento(prevBoxes,rect,xRange):
        #No hay necesidad de probar que las boxes anteriores estaban dentro de la región 
        #Boxes anteriores son confiables, es decir, se encontraban previamente dentro de la región

        for prev in prevBoxes:
            xLimA1 = prev[0] - xRange
            xLimA2 = prev[0] + xRange
            
            yLimA1 = prev[1] - xRange
            yLimA2 = prev[1] + xRange
            
            xLimB1 = prev[2] - xRange
            xLimB2 = prev[2] + xRange
            
            yLimB1 = prev[3] - xRange
            yLimB2 = prev[3] + xRange
            
            if(xLimA1<rect[0] and rect[0]<xLimA2 and yLimA1<rect[1] and rect[1]<yLimA2 
               and xLimB1<rect[2] and rect[2]<xLimB2 and yLimB1<rect[3] and rect[3]<yLimB2):
              return False # No hubo mucho cambio en el movimiento comparado con el frame anterior
        else:
              return True
        
    
    # Nos servira para obterner el fondo
    fondo = None
    
    # Recorremos todos los frames
    while(1):
      _,frame = cap.read() #Leer un frame
      frame2 = np.copy (frame)
      gris = colorChange(frame)
      gris = colorFilter(gris)
     
      
    # Aplicamos suavizado para eliminar el ruido
      gris = cv2.GaussianBlur(gris, (21, 21), 0)
      
    # Si todavia no hemos obtenido el fondo, lo obtenemos
      if fondo is None:
          fondoanterior = gris
          fondo = gris
          continue
      else:
          fondo = fondoanterior      
      
    # Calculo la dif etre el fondo y el frame
      resta = cv2.absdiff(fondo, gris)
     
    # Aplicamos un umbral
      umbral = cv2.threshold(resta, m, 255, cv2.THRESH_BINARY)[1]
     
    # Dilatamos el umbral para tapar agujeros
      umbral = cv2.dilate(umbral, None, iterations=2)
     
    # Copiamos el umbral para detectar los contornos
      contornosimg = umbral.copy()
      
    # Buscamos contorno en la imagen
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
      
      print cajas
            
      if not prevBoxes:
           prevBoxes = cajas
           pass
                    
      # Define si hay movimiento dentro de las regiones
      if cajas == []:
          inHandsnoMov = 0
          outHands = 0
          exitHands+=1
          chrono = 0
          if exitHands == 10: # No se detectaron manos durante 30 ciclos
              print "No hay manos qué detectar"
              reason = 3
              cap.release()
              cv2.destroyAllWindows()
              for i in range (1,10):
                  cv2.waitKey(1)
              return False, reason
              break
          else:
              cv2.rectangle(image2, (regionCoordinates[0], regionCoordinates[1]), (regionCoordinates[2], regionCoordinates[3]), (255, 0, 255), 2) # Con las coordenadas construye el rectángulo
              cv2.imshow("other", image2)
              fondoanterior = gris
              prevBoxes = cajas
              k = cv2.waitKey(5) & 0xFF
              time.sleep(0.015)
              continue
      else:     
          for rect in cajas:
              overlap = overlapRectangles(regionCoordinates,rect)
              if overlap: # overlap quiere decir que las cajas detectadas se sobreponen a la de la región
                  exitHands = 0
                  outHands = 0
                  inHandsnoMov = 0
                  c = umbralMovimiento(prevBoxes,rect,xRange)
                               
                  if c: # Hubo movimiento significativo
                      if chrono == 0:
                          chrono = currentTime()
                          prevBoxes = cajas
                          print "Hay movimiento en la region ", noRegion
                          pass
                      else:
                          chrono_aux = currentTime()
                          if (chrono_aux - chrono) >= tiempo: #Hubo movimiento durante el tiempo suficiente
                              reason = 1
                              cap.release()
                              cv2.destroyAllWindows()
                              for i in range (1,10):
                                cv2.waitKey(1)
                              return True, reason
                              break
                  else: # No hubo movimiento significativo
                      chrono = 0
                      outHands = 0
                      exitHands = 0
                      inHandsnoMov+=1
                      if inHandsnoMov == 10: # Si no hubo movimiento significativo durante 50 ciclos
                          print "Debido a que no ha seguido el procedimiento deberá recomenzar"
                          reason = 2
                          cap.release()
                          cv2.destroyAllWindows()
                          for i in range (1,10):
                            cv2.waitKey(1)
                          return False, reason
                          break
                                        
                     
              else: # No se sobreponen pero sí se detectan cajas
                  chrono = 0
                  inHandsnoMov = 0
                  exitHands = 0
                  if outHands == 1:
                      print 'No hay presencia en la región Por favor hagalo mejor.'
                  outHands+=1
                  if outHands == 10:  # Se detectaron manos en el lugar incorrecto durante 30 ciclos
                      reason = 4
                      cap.release()
                      cv2.destroyAllWindows()
                      for i in range (1,10):
                          cv2.waitKey(1)
                      return False, reason
                      break
                      
             
      cv2.rectangle(image2, (regionCoordinates[0], regionCoordinates[1]), (regionCoordinates[2], regionCoordinates[3]), (255, 0, 255), 2) # Con las coordenadas construye el rectángulo
   
      #Mostrar los resultados y salir
      
      #cv2.imshow('camara',frame)
      #cv2.imshow('gris',gris)
      #cv2.imshow("Umbral", umbral)
      #cv2.imshow("Resta", resta)
      #cv2.imshow("Contorno", contornosimg)
      cv2.imshow("other", image2)
      
      fondoanterior = gris
      prevBoxes = cajas

      k = cv2.waitKey(5) & 0xFF
  
  #tiempo de espera para que se vea bien
      time.sleep(0.015)
    
  #si ha pulsado escape para salir, salimos
      if k == 27:
    #liberamos la camara y cerramos todas las ventanas
        cap.release()
        cv2.destroyAllWindows()
        for i in range (1,10):
            cv2.waitKey(1)

