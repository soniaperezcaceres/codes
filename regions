    # -*- coding: utf-8 -*-

def funcionRegiones(regionsNumber):
    
    def on_mouse(event,x,y,flags,params):
    
        global rect,startPoint,endPoint, ix, iy, dragnDrop, releaseRectangle, regionCount, regionPoints, regionDone
        
        if event == cv2.EVENT_LBUTTONDBLCLK: # When mouse click...
    
            if startPoint == True and endPoint == True: 
                startPoint = False
                endPoint = False
                rect = (0, 0, 0, 0)
    
            if startPoint == False: # Primer click, vuelve starPoint TRUE para 'asegurarse de que ya tomó la primera coordenada'
                rect = (x, y, 0, 0)
                startPoint = True
                
            elif endPoint == False: # Como ya starPoint esta en TRUE, esta condicion se cumple y ahora endPoint pasa a ser TRUE tambien  
                if rect[0]<x: # Esto fue lo que agregué: arregla el array de tal manera que quede uniforme sin
                    if rect[1]<y: # importar el orden en el que se hayan definido las esquinas de la región
                        rect = (rect[0], rect[1], x, y) 
                    else:
                        rect = (rect[0], y, x, rect[1])
                else:
                    if rect[1]<y:
                        rect = (x, rect[1], rect[0], y)
                    else:
                        rect = (x, y, rect[0], rect[1])
                #rect = (rect[0], rect[1], x, y) # Conserva las coordernadas de starPoint y añade las de endPoint
                dragnDrop == False
                regionPoints[regionCount][0] = rect[0]
                regionPoints[regionCount][1] = rect[1]
                regionPoints[regionCount][2] = rect[2]
                regionPoints[regionCount][3] = rect[3]
                #print regionPoints[:][:]
                regionCount = regionCount + 1
                #print startPoint
                endPoint = True
                regionDone = True
                #print regionCount
    
        if event == cv2.EVENT_MOUSEMOVE and startPoint == True and endPoint == False: # When  mouse moves...
            dragnDrop = True
            ix,iy = x,y
                       
        if event == cv2.EVENT_RBUTTONDOWN and dragnDrop == True: # Cuando haces right click y se está Drag n' Dropin', se suelta el rectangulo
            releaseRectangle = True
            ix,iy = x,y
    
    
    
    import cv2    
    global rect,regionsNo, startPoint,endPoint, ix, iy, dragnDrop, releaseRectangle, regionCount, regionPoints, regionDone
    waitTime = 50
    regionsNo = regionsNumber
    cap = cv2.VideoCapture(0)
    cap.set(3,320)
    cap.set(4,240)
    rect = (0,0,0,0)
    startPoint = False
    endPoint = False
    dragnDrop = False
    releaseRectangle = False
    regionDone = False 
    ix, iy = -1, -1
    regionCount = 0
    rgX, rgY = 4, regionsNo;
    regionPoints = [[0 for xi in range(rgX)] for yi in range(rgY)]
    
    (grabbed, frame) = cap.read() #Reading the first frame
    
    while(cap.isOpened()):
    
        (grabbed, frame) = cap.read()
    
        cv2.namedWindow('frame')
        cv2.setMouseCallback('frame', on_mouse)    
        
        # Dibujar el Drag n' Drop
        if startPoint == True and endPoint == False: # Primer click, vuelve starPoint TRUE para 'asegurarse de que ya tomo la primera coordenada'
            cv2.rectangle(frame, (rect[0], rect[1]), (ix, iy), (255, 0, 255), 2) # Con las coordenadas construye el rectángulo
            
        # Dibujar el rectángulo
        if regionDone == True:
            for rects in range (0,regionCount):
                cv2.rectangle(frame, (regionPoints[rects][0], regionPoints[rects][1]), (regionPoints[rects][2], regionPoints[rects][3]), (255, 0, 255), 2) # Con las coordenadas construye el rectángulo
        
        # Desdibujar el Drag n' Drop
        if dragnDrop == True and releaseRectangle == True: 
            startPoint = False
            endPoint = False
            releaseRectangle = False
            dragnDrop = False
            cv2.rectangle(frame, (0,0),(0,0), (255, 0, 255), 2) # Con las coordenadas construye el rectangulo
    
        cv2.imshow('frame',frame)
    
        key = cv2.waitKey(waitTime) 
    
        if key == 27:
            cv2.VideoCapture(0).release()
            break
        
        if regionCount == regionsNo:
            #cv2.VideoCapture(0).release()
            break
        
        
    cap.release()
    cv2.destroyAllWindows()
    return regionPoints
