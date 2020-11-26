# -*- coding: utf-8 -*-
from Tkinter import Tk, Label, Button, Toplevel, PhotoImage
import contadorMovimiento, colorPiel, regions, BByOFfile
import time, datetime, PIL, cv2, os, threading, xlsxwriter
from PIL import Image, ImageTk
from functools import partial
from threading import Thread
import numpy as np
from Queue import Queue
import detectUser

######################## DOCUMENTO

# Create a workbook and add a worksheet.
workbook = xlsxwriter.Workbook('REGISTRO.xlsx')
worksheet = workbook.add_worksheet()

#today date
date_time = datetime.datetime.now()

#format for the cells
f1= workbook.add_format({'bold': True, 'font_color':'red', 'center_across':True})
f2= workbook.add_format({'num_format':'d mmm yyyy', 'center_across':True})
f3= workbook.add_format({'num_format':'hh:mm:ss', 'center_across':True})
f4= workbook.add_format({'bold': True, 'center_across':True})
f5= workbook.add_format({'bold': True})
f6= workbook.add_format({'center_across':True})

row=0
col=0
cont=0

#datos del documento 
worksheet.write('A1', 'FECHA', f1)
worksheet.write('B1', 'HORA', f1)
worksheet.write('C1', 'PERSONA', f1)
worksheet.write('D1', 'CALFICACION', f1)

######################## INTERFAZ GRAFICA 

ventana = Tk() # Initializes interpreter and creates root window
ventana.title('HELLO MANITOR') # Name of the window
ventana.configure(bg="white") # Background color
ventana.geometry("400x270+100+100") # Size of the window
ventana2= None 
Labelt=None
label=Label(ventana,text="BIENVENIDO",
             fg="red",bg="white",font=("Helvetica 24 bold"))
label.grid(row=1,column=1)

######################## LABEL REGIONES + FUNC REGIONES + BOTON REGIONES

labelregiones=Label(ventana,
             text="Por favor seleccione las regiones correspondientes",
             fg="black",bg="white",font=("Helvetica 12"))
labelregiones.grid(row=2,column=1)

numberOfRegions = 2

def regiones():
    global regionCoord
    regionCoord = regions.funcionRegiones(numberOfRegions)
    print regionCoord
    
botonregiones = Button(ventana,text="REGIONES", command=regiones,
                fg="white",bg='red',font=("Helvetica 12 bold"))
botonregiones.grid(row=3,column=1)

######################## LABEL COLOR + FUNC COLOR + BOTON COLOR

labelcolor=Label(ventana,
             text="Por favor seleccione un rango de color",
             fg="black",bg="white",font=("Helvetica 12 "))
labelcolor.grid(row=4,column=1)

def color():
    global lower,upper   
    import numpy as np
    hMin = 8
    hMax = 17
    sMin = 27 
    sMax = 92
    vMin = 76
    vMax = 255
    lower=np.array([hMin,sMin,vMin])
    upper=np.array([hMax,sMax,vMax])
#    lower, upper = colorPiel.funcionColor()

botoncolor = Button(ventana,text="COLOR", command=color,
                fg="white",bg='red',font=("Helvetica 12 bold"))
botoncolor.grid(row=5,column=1)

######################## VIDEOS

v1 = cv2.VideoCapture('1.mp4')
v2 = cv2.VideoCapture('2.mp4')
v00 = cv2.VideoCapture('00.mp4')
v000 = cv2.VideoCapture('000.mp4')

def stream(label,v1):
    global ventana2
    v1.set(1,0)
    ventana2.update()
    while True:
        ok, frame = v1.read()
        if not ok:
            break
        key = cv2.waitKey(1) 
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        current_image = Image.fromarray(cv2image)  
        imgtk = ImageTk.PhotoImage(image=current_image)   
        label.image = imgtk        
        label.config(image=imgtk)
        ventana2.update()

def video1():
    global Labeli,v1
    ventana2.update()
    stream(Labeli,v1)
    
def video2():
    global Labeli,v2
    ventana2.update()
    stream(Labeli,v2)
    
def video00():
    global Labeli,v00
    ventana2.update()
    stream(Labeli,v00)

def video000():
    global Labeli,v000
    ventana2.update()
    stream(Labeli,v000)

############################################## DEFINIR FUNCIONES
queue = Queue()

errorCount = 0

def jabon():
    global errorCount
    if errorCount >= 3:
        errorCount = 0
        inicio(0)
    
    def cero(q):
        analysisRegion = 1
        print regionCoord
        tipoMovimiento=BByOFfile.BByOF(2,lower,upper,regionCoord,analysisRegion,10)
        q.put([tipoMovimiento])            

    Labelt.config(text='Deposite jabón en la mano')
    global row
    row=row+1
    worksheet.write(row, col +3, 'jabon', f5)
    ventana2.update()      
    c=threading.Thread(target=cero, args=(queue,))
    c.start()
    video00()       

    if c.isAlive():
        c.join()
    instruction=queue.get()
    instruction=falseType(instruction[0],Labelt,Labeli,img0,imgF)        
    if not instruction:
        errorCount = errorCount + 1
        jabon()


def primero1():
    global errorCount
    if errorCount >= 3:
    errorCount = 0
    inicio(0)
        
    def primero(q):
        analysisRegion = 2
        tipoMovimiento=BByOFfile.BByOF(2,lower,upper,regionCoord,analysisRegion,10) 
        q.put([tipoMovimiento])
       
    p=Thread(target=primero, args=(queue,))
    p.start()
    Labelt.config(text='Frote las palmas de las manos \n entre sí')
    global row
    row=row+1
    worksheet.write(row, col +3, 'instruccion1', f5)
    ventana2.update()
    ventana2.update()
    video1()

    if p.isAlive():
        p.join()
    instruction=queue.get()
    instruction=falseType(instruction[0],Labelt,Labeli,img0,imgF) 
    if not instruction:
        primero1()


##        def segundo(q):
##            global errorCount
##            if errorCount >= 3:
##              errorCount = 0
##              inicio(0)
##            analysisRegion = 2
##            tipoMovimiento=BByOFfileO.BByOF(2,lower,upper,regionCoord,analysisRegion,10)
##            q.put([tipoMovimento])
##               
##        s=Thread(target=segundo, args=(queue,))
##        s.start()
##        Labelt.config(text='Frote la palma de la mano derecha \n contra el dorso de la mano izquierda  \n entrelazando los dedos y viceversa')
##        ventana2.update()
##        video2()
##      
##        if s.isAlive():
##            s.join()
##        instruction=queue.get()
##        instruction=falseType(instruction[0],Labelt,Labeli,img0,imgF) 
##        if not instruction:
##            inicio(0)

        
######################## LABEL INICIO + FUNC INICIO + BOTON INICIO

labelinicio=Label(ventana,
             text="Ahora puede iniciar",
             fg="black",bg="white",font=("Helvetica 12 "))
labelinicio.grid(row=6,column=1) 

######################## AUXILIAR


def falseType(tipoMovimiento,Labelt,Labeli,img0,imgF):
    global row
    
    if tipoMovimiento == 1:
        Labeli.image = img0  
        Labeli.config(image=img0)
        Labelt.config(text='Cumplió con el tiempo requerido')
        row=row+1
        worksheet.write(row, col +3, 'bien')
        ventana2.update()
        ventana2.after(2000)
        return True
                
    elif tipoMovimiento == 0:
        Labeli.image = imgF    
        Labeli.config(image=imgF)
        Labelt.config(text="No se detectó movimiento de sus manos \n Vuelva a empezar")
        row=row+1
        worksheet.write(row, col +3, 'mal1')
        ventana2.update()
        ventana2.after(2000)
        return False


######################## ....................... #######################

def inicio(c):
    global ventana2, Labeli, Labelt, img0, img1, imgF, row, cont
    instruction=None
    img0=PhotoImage(file="00.gif") # Reads photos
    img00=PhotoImage(file="0000.gif")
    imgF=PhotoImage(file="FF.gif")

    if c:  
        ventana2=Toplevel(ventana)
        ventana2.title("MANITOR")
        ventana2.configure(bg="white")
        ventana2.geometry("1000x600+5+40")
    
        Labelt=Label(ventana2,text='BIENVENIDO ', # ventana2 TEXTO
                fg="black",bg="white",font=("Helvetica 36 "))
        ventana2.columnconfigure(0,weight=1)
        Labelt.grid(row=1,column=0)
        Labeli=Label(ventana2,image=img00) # ventana2 IMAGEN
        Labeli.grid(row=2,column=0)
                
    else:
        Labelt.config(text='BIENVENIDO ')
        Labeli.image = img00
        Labeli.config(image=img00)
    ventana.iconify() # Turns window into an icon
    
    row=row+1
    cont=cont+1

    

    
    while 1:
        
        nuevoUsuario = detectUser.newUser(3,lower,upper)
        
    
        Labelt.config(text='BIENVENIDO \n  Por favor moje sus manos con agua')
        worksheet.write_datetime(row, col, date_time,f2)
        worksheet.write_datetime(row, col+1, date_time,f3)
        worksheet.write(row, col +2, cont, f6)
        worksheet.write(row, col +3, 'NUEVA PERSONA',f4)
        ventana2.update()
        video000()


        jabon()        

        primero1()
            
####################### fin instrucciones

        Labeli=Label(ventana2,image=img00)
        Labeli.grid(row=2,column=0)
        Labelt.config(text='Sus manos son seguras')
        row=row+1
        worksheet.write_datetime(row, col, date_time, f2)
        worksheet.write_datetime(row, col+1, date_time,f3)
        worksheet.write(row, col +3, 'TERMINO')
        ventana2.update()
        ventana2.after(2000)

######################## ........................ ######################  

inicio_arg=partial(inicio,1)
botoninicio = Button(ventana,text="INICIAR",fg="white",command=inicio_arg,
                     bg='red',font=("Helvetica 12 bold"))
botoninicio.grid(row=7,column=1)

######################## LABEL FIN + FUNC FIN + BOTON FIN 

labelfin=Label(ventana,
             text="si desea finalizar",
             fg="black",bg="white",font=("Helvetica 12 "))
labelfin.grid(row=8,column=1)

def finalizar():
    workbook.close()
    ventana2.destroy()

botonfin = Button(ventana,text="FIN",fg="white",command=finalizar,
                     bg='red',font=("Helvetica 12 bold"))
botonfin.grid(row=9,column=1)

######################################################################
ventana.mainloop()
