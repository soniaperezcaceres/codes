# -*- coding: utf-8 -*-
from Tkinter import Tk, Label, Button, Toplevel, PhotoImage
import contadorMovimiento, colorPiel, regions
import time, PIL, cv2, os, threading
from PIL import Image, ImageTk
from functools import partial
from threading import Thread
import psycopg2

######################## BASE DE DATOS

con = psycopg2.connect("dbname='prueba1' user='postgres' password='hola'")
cur = con.cursor()
cur.execute("CREATE TABLE manitor(Id SERIAL PRIMARY KEY, fecha_hora TIMESTAMP default now(), calificacion VARCHAR(200))")
cur.execute("CREATE SEQUENCE usuario_sequence start 1 increment 1")
cur.execute("SET TIME ZONE 'GMT+5'")

######################## INTERFAZ GRAFICA 

ventana = Tk() # Initializes interpreter and creates root window
ventana.title('HELLO MANITOR') # Name of the window
ventana.configure(bg="white") # Background color
ventana.geometry("400x330+100+100") # Size of the window
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

def regiones():
    global y
    y = regions.funcionRegiones(2)
    #print y
    
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
    lower, upper = colorPiel.funcionColor()

botoncolor = Button(ventana,text="COLOR", command=color,
                fg="white",bg='red',font=("Helvetica 12 bold"))
botoncolor.grid(row=5,column=1)

######################## VIDEOS

def video1():
    v1 = cv2.VideoCapture('1.mp4')
    current_image = None
    def videoloop1():
        ventana2.update()
        ok, frame = v1.read()  
        if ok:  
            key = cv2.waitKey(1)
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            current_image1 = Image.fromarray(cv2image)  
            imgtk = ImageTk.PhotoImage(image=current_image)   
            panel.imgtk = imgtk    
            panel.config(image=imgtk)  
        ventana2.after(1,videoloop1)
    panel = Label(ventana2)
    panel.grid(row=2,column=0)
    videoloop1()
    ventana2.update()
    
def video2():
    v2 = cv2.VideoCapture('2.mp4')
    current_image = None
    def videoloop2():
        ventana2.update()
        ok, frame = v2.read()  
        if ok:  
            key = cv2.waitKey(1)
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            current_image2 = Image.fromarray(cv2image)  
            imgtk = ImageTk.PhotoImage(image=current_image)   
            panel.imgtk = imgtk   
            panel.config(image=imgtk)  
        ventana2.after(1,videoloop2)
    panel = Label(ventana2)
    panel.grid(row=2,column=0)
    videoloop2()
    ventana2.update()

def video00():
    v00 = cv2.VideoCapture('00.mp4')
    current_image = None
    def videoloop00():
        ventana2.update()
        ok, frame = v00.read()  
        if ok:  
            key = cv2.waitKey(1)
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            current_image = Image.fromarray(cv2image)  
            imgtk = ImageTk.PhotoImage(image=current_image)   
            panel.imgtk = imgtk  
            panel.config(image=imgtk)  
        ventana2.after(1,videoloop00)
    panel = Label(ventana2)
    panel.grid(row=2,column=0)
    videoloop00()
    ventana2.update

def video000():
    v000 = cv2.VideoCapture('000.mp4')
    current_image = None
    def videoloop000():
        ventana2.update()
        ok, frame = v000.read()  
        if ok:  
            key = cv2.waitKey(1)
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            current_image = Image.fromarray(cv2image)  
            imgtk = ImageTk.PhotoImage(image=current_image)   
            panel.imgtk = imgtk    
            panel.config(image=imgtk)  
        ventana2.after(1,videoloop000)  
    panel = Label(ventana2)
    panel.grid(row=2,column=0)
    videoloop000()
    ventana2.update()

######################## LABEL INICIO + FUNC INICIO + BOTON INICIO

labelinicio=Label(ventana,
             text="Ahora puede iniciar",
             fg="black",bg="white",font=("Helvetica 12 "))
labelinicio.grid(row=6,column=1) 

######################## AUXILIAR

def falseType(falseb,auxVariable,Labelt,Labeli,img0,imgF):
    
    if falseb:

        Labeli=Label(ventana2,image=img0)
        Labeli.grid(row=2,column=0)
        Labelt.config(text='Cumplió con el tiempo requerido')
        cur.execute("INSERT INTO manitor VALUES(nextval('usuario_sequence'), now(), 'cumplio con el tiempo en jabon')")
        ventana2.update()
        ventana2.after(5000)
        print 'bien'
        return True
        
        
    elif auxVariable == 2:

        Labeli=Label(ventana2,image=imgF)
        Labeli.grid(row=2,column=0)
        Labelt.config(text="No se detectó movimiento de sus manos \n Vuelva a empezar")
        cur.execute("INSERT INTO manitor VALUES(nextval('usuario_sequence'), now(), 'No hubo suficiente movimiento de las manos')")
        ventana2.update()
        ventana2.afer(5000)
        print 'mal'
        return False

        
    elif auxVariable == 3:

        Labeli=Label(ventana2,image=imgF)
        Labeli.grid(row=2,column=0)
        Labelt.config(text="No se detectaron sus manos \n Vuelva a empezar")
        cur.execute("INSERT INTO manitor VALUES(nextval('usuario_sequence'), now(), 'No se detectaron las manos')")
        ventana2.update()
        ventana2.after(5000)
        print 'mal'
        return False
        

    elif auxVariable == 4:

        Labeli=Label(ventana2,image=imgF)
        Labeli.grid(row=2,column=0)
        Labelt.config(text="No se detectaron sus manos dentro de la región de lectura \n Vuelva a empezar")
        cur.execute("INSERT INTO manitor VALUES(nextval('usuario_sequence'), now(), ' No se registraron manos dentro de la region')")
        ventana2.update()
        ventana2.after(5000)
        print 'mal'
        return False      

######################## ....................... #######################

def inicio(c):
    global ventana2, Labeli, Labelt
    global img0, img1, imgF
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
        print 'empezo'
                
    else:
        Labelt.config(text='BIENVENIDO ')
        Labeli=Label(ventana2,image=img00)
        Labeli.grid(row=2,column=0)
    ventana.iconify() # Turns window into an icon

    while 1:

        cur.execute("INSERT INTO manitor VALUES(nextval('usuario_sequence'), current_timestamp, 'nuevo usuario')")
        print 'empezo 1'
        Labelt.config(text='BIENVENIDO \n  Por favor moje sus manos con agua')
        ventana2.update()
        video000                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     ()
        ventana2.update()
        
        def cero():
            b,auxType = contadorMovimiento.funcionMovimientoEnRegion(y[1],3,2,lower,upper) 
            instruction = falseType(b,auxType,Labelt,Labeli,img0,imgF)
            if not instruction:
                inicio(0)
       
        Thread(target=cero).start()
        Thread(target=video00()).start()
        
        print 'paso 0'
        cur.execute("INSERT INTO manitor VALUES(nextval('usuario_sequence'), current_timestamp, ' jabon bien  ')")
        
        Labelt.config(text='Deposite jabón en la mano')
        ventana2.update()

######################## instruccion 1
        
        def primero():
            d,auxType = contadorMovimiento.funcionMovimientoEnRegion(y[1],3,2,lower,upper) 
            instruction = falseType(d,auxType,Labelt,Labeli,img0,imgF)
            if not instruction:
                inicio(0)
                
        Thread(target=primero).start()
        Thread(target=video1()).start()

        print 'paso 1'
        cur.execute("INSERT INTO manitor VALUES(nextval('usuario_sequence'), current_timestamp, 'paso 1 bien')")

        Labelt.config(text='Frote las palmas de las manos \n entre sí')
        ventana2.update()

########################## instruccion2

        def segundo():
            e,auxType = contadorMovimiento.funcionMovimientoEnRegion(y[1],10,2,lower,upper) 
            instruction = falseType(e,auxType,Labelt,Labeli,img0,imgF)
            if not instruction:
                inicio(0)
                
        Thread(target=segundo).start()
        Thread(target=video2()).start()
        
        Labelt.config(text='Frote la palma de la mano derecha \n contra el dorso de la mano izquierda  \n entrelazando los dedos y viceversa')
        panel = Label(ventana2)
        print 'paso 2'
        cur.execute("INSERT INTO manitor VALUES(nextval('usuario_sequence'), current_timestamp, ' nuevo usuario ')")

######################## fin instrucciones

        Labeli=Label(ventana2,image=img00)
        Labeli.grid(row=2,column=0)
        Labelt.config(text='Sus manos son seguras')
        ventana2.update()
        ventana2.after(5000)
        print 'fin bien'
        cur.execute("INSERT INTO manitor VALUES(nextval('usuario_sequence'), current_timestamp, ' termino bien ')")

######################## ........................ ######################  

inicio_arg=partial(inicio,1)
botoninicio = Button(ventana,text="INICIAR",fg="white",command=inicio_arg,
                     bg='red',font=("Helvetica 12 bold"))
botoninicio.grid(row=7,column=1)

######################## LABEL BASE + FUNC BASE + BOTON BASE

labelbase=Label(ventana,
             text="base de datos",
             fg="black",bg="white",font=("Helvetica 12 "))
labelbase.grid(row=8,column=1)

def basesita():
    cur.execute("SELECT * FROM manitor")
    resultados = cur.fetchall()
    for i in resultados:
        print i

botonbase = Button(ventana,text="BASEDATOS",fg="white",command=basesita,
                     bg='red',font=("Helvetica 12 bold"))
botonbase.grid(row=9,column=1)

######################## LABEL FIN + FUNC FIN + BOTON FIN 

##labelfin=Label(ventana,
##             text="si desea finalizar",
##             fg="black",bg="white",font=("Helvetica 12 "))
##labelfin.grid(row=8,column=1)
##
##def finalizar():
##    ventana2.destroy()
##
##botonfin = Button(ventana,text="FIN",fg="white",command=finalizar,
##                     bg='red',font=("Helvetica 12 bold"))
##botonfin.grid(row=9,column=1)

######################################################################

ventana.mainloop()
