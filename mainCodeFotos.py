# -*- coding: utf-8 -*-
from Tkinter import Tk, Label, Button, Toplevel, PhotoImage
import contadorMovimiento, colorPiel, regions
import time, PIL, cv2, os, threading
from PIL import Image, ImageTk
from functools import partial
from threading import Thread
import psycopg2

#from Tkinter import *
from Tkinter import Tk, Label, Button, Toplevel, PhotoImage

######################## BASE DE DATOS

con = psycopg2.connect("dbname='prueba1' user='postgres' password='hola'")
cur = con.cursor()
cur.execute("CREATE TABLE manitor(Id SERIAL PRIMARY KEY, fecha_hora TIMESTAMP default now(), calificacion VARCHAR(200))")
cur.execute("CREATE SEQUENCE usuario_sequence start 1 increment 1")
cur.execute("SET TIME ZONE 'GMT+5'")

###########################################

ventana = Tk() # Initializes interpreter and creates root window
ventana.title('HELLO MANITOR') # Name of the window
ventana.configure(bg="white") # Background color
ventana.geometry("400x330+100+100") # Size of the window
ventana2= None 
Labelt=None
label=Label(ventana,text="BIENVENIDO",
             fg="red",bg="white",font=("Helvetica 24 bold"))
label.grid(row=1,column=1)

############################################ ETIQUETA 1 + BOTON 1

labelregiones=Label(ventana,
             text="Por favor seleccione las regiones correspondientes",
             fg="black",bg="white",font=("Helvetica 12"))
labelregiones.grid(row=2,column=1)

def regiones():
    global y
    y = regions.funcionRegiones(2)
    print y
botonregiones = Button(ventana,text="REGIONES", command=regiones,
                fg="white",bg='red',font=("Helvetica 12 bold"))
botonregiones.grid(row=3,column=1)

########################################### ETIQUETA 2 + BOTON 2

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

############################################ ETIQUETA 3 + BOTON 3

labelinicio=Label(ventana,
             text="Ahora puede iniciar",
             fg="black",bg="white",font=("Helvetica 12 "))
labelinicio.grid(row=6,column=1)


def falseType(falseb,auxVariable,Labelt,Labeli,img0,imgF):

    if falseb:
        Labelt.config(text='Cumplió con el tiempo requerido')
##        Labeli=Label(ventana2,image=img0)
##        Labeli.grid(row=2,column=0)
        Labeli.config(image=img0)
##        Labeli.image=img0
        cur.execute("INSERT INTO manitor VALUES(nextval('usuario_sequence'), now(), 'cumplio con el tiempo en jabon')")
        ventana2.update()
        time.sleep(2)
        return True   
        
    elif auxVariable == 2:       
        Labelt.config(text="No se detectó movimiento de sus manos \n Vuelva a empezar")
        Labeli.config(image=imgF)
        cur.execute("INSERT INTO manitor VALUES(nextval('usuario_sequence'), now(), 'No hubo suficiente movimiento de las manos')")
        ventana2.update()
        time.sleep(2)
        return False
        
    elif auxVariable == 3:        
        Labelt.config(text="No se detectaron sus manos \n Vuelva a empezar")
        Labeli.config(image=imgF)
        cur.execute("INSERT INTO manitor VALUES(nextval('usuario_sequence'), now(), 'No se detectaron las manos')")
        ventana2.update()
        time.sleep(2)
        return False       

    elif auxVariable == 4:        
        Labelt.config(text="No se detectaron sus manos dentro de la región de lectura \n Vuelva a empezar")
        Labeli.config(image=imgF)
        cur.execute("INSERT INTO manitor VALUES(nextval('usuario_sequence'), now(), ' No se registraron manos dentro de la region')")
        ventana2.update()
        time.sleep(2)
        return False
        
def inicio(c):
    global ventana2
    global Labeli
    global Labelt
    img0=PhotoImage(file="00.gif") # Reads photos
    img1=PhotoImage(file="11.gif")
    img2=PhotoImage(file="22.gif")
    img3=PhotoImage(file="33.gif")
    img4=PhotoImage(file="44.gif")
    img12=PhotoImage(file="1212.gif")
    imgF=PhotoImage(file="FF.gif")
    
    if c:  
        ventana2=Toplevel(ventana)
        ventana2.title("MANITOR")
        ventana2.configure(bg="white")
        ventana2.geometry("1000x600+5+40")
    
        Labelt=Label(ventana2,text='BIENVENIDO ', # ventana2 TEXTO
                fg="black",bg="white",font=("Helvetica 36 "))
        ventana2.columnconfigure(0,weight=1)
        Labelt.grid(row=1,column=0) # Organizes widgets in blocks before placing them in the parent widget
        
        
        Labeli=Label(ventana2,image=img1) # ventana2 IMAGEN
        Labeli.grid(row=2,column=0)
        
    else:
        Labelt.config(text='BIENVENIDO ')
        Labeli.config(image=img1)
    ventana.iconify() # Turns window into an icon

    while 1:

        cur.execute("INSERT INTO manitor VALUES(nextval('usuario_sequence'), current_timestamp, ' inicio ')")
        
        Labelt.config(text='BIENVENIDO \n  Por favor moje sus manos con agua')
        Labeli.config(image=img1)
        ventana2.update()
        time.sleep(2)
        
        Labelt.config(text='Deposite jabón en la mano')
        cur.execute("INSERT INTO manitor VALUES(nextval('usuario_sequence'), current_timestamp, ' nuevo usuario ')")
        Labeli.config(image=img2)
        ventana2.update()
        time.sleep(0.5)
        b,auxType = contadorMovimiento.funcionMovimientoEnRegion(y[1],3,2,lower,upper) 
                     
        # Llamar la función de
        instruction = falseType(b,auxType,Labelt,Labeli,img0,imgF)
        if not instruction:
            inicio(0)

        Labelt.config(text='Frote las palmas de las manos \n entre sí')
        Labeli.config(image=img3)
        ventana2.update()
        time.sleep(0.5)
        d,auxType = contadorMovimiento.funcionMovimientoEnRegion(y[0],0.5,1,lower,upper)        

        instruction = falseType(d,auxType,Labelt,Labeli,img0,imgF)
        if not instruction:
            inicio(0)

        Labelt.config(text='Frote la palma de la mano derecha \n contra el dorso de la mano izquierda  \n entrelazando los dedos y viceversa')
        Labeli.config(image=img4)
        ventana2.update()
        time.sleep(0.5)
        e,auxType = contadorMovimiento.funcionMovimientoEnRegion(y[0],0.5,1,lower,upper)        

        instruction = falseType(e,auxType,Labelt,Labeli,img0,imgF)
        if not instruction:
            inicio(0)

        Labelt.config(text='Sus manos son seguras')
        cur.execute("INSERT INTO manitor VALUES(nextval('usuario_sequence'), current_timestamp, ' termino bien ')")
        Labeli.config(image=img12)
        ventana2.update()
        time.sleep(5)
    
inicio_arg=partial(inicio,1)
botoninicio = Button(ventana,text="INICIAR",fg="white",command=inicio_arg,bg='red',font=("Helvetica 12 bold"))
#botoninicio.bind('<Button-1>', inicio_arg)
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

####################################

ventana.mainloop()
