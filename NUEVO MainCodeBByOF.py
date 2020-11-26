# -*- coding: utf-8 -*-
from Tkinter import Tk, Label, Button, Toplevel, PhotoImage
import contadorMovimiento, colorPiel, regions 
import time, PIL, cv2, os, threading #psycopg2
from PIL import Image, ImageTk
from functools import partial
from threading import Thread

######################## BASE DE DATOS

##con = psycopg2.connect("dbname='prueba1' user='postgres' password='hola'")
##cur = con.cursor()
##cur.execute("CREATE TABLE manitor(Id SERIAL PRIMARY KEY, fecha_hora TIMESTAMP default now(), calificacion VARCHAR(200))")
##cur.execute("CREATE SEQUENCE usuario_sequence start 1 increment 1")
##cur.execute("SET TIME ZONE 'GMT+5'")

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
def video0():
    v0 = cv2.VideoCapture('0.mp4') # capture video frames
    current_image = None  # current image from the camera
    def videoloop0():
        ventana2.update()
        ok, frame = v0.read()  # read frame from video stream
        if ok:  # frame captured without any errors
            key = cv2.waitKey(1)
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            current_image = Image.fromarray(cv2image)  # convert image for PIL
            imgtk = ImageTk.PhotoImage(image=current_image)  # convert image for tkinter 
            panel.imgtk = imgtk  # anchor imgtk so it does not be deleted by garbage-collector  
            panel.config(image=imgtk)  # show the image
        ventana2.after(1,videoloop0)  # call the same function after 30 milliseconds
    panel = Label(ventana2)
    ventana2.columnconfigure(0,weight=1)
    panel.grid(row=2,column=0)
    videoloop0()
    ventana2.update()

def video1():
    v1 = cv2.VideoCapture('1.mp4')
    current_image = None
    def videoloop1():
        ventana2.update()
        ok, frame = v1.read()  
        if ok:  
            key = cv2.waitKey(1)
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            current_image = Image.fromarray(cv2image)  
            imgtk = ImageTk.PhotoImage(image=current_image)   
            panel.imgtk = imgtk    
            panel.config(image=imgtk)  
        ventana2.after(1,videoloop1)
    panel = Label(ventana2)
    ventana2.columnconfigure(0,weight=1)
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
            current_image = Image.fromarray(cv2image)  
            imgtk = ImageTk.PhotoImage(image=current_image)   
            panel.imgtk = imgtk    
            panel.config(image=imgtk)  
        ventana2.after(1,videoloop2)
    panel = Label(ventana2)
    ventana2.columnconfigure(0,weight=1)
    panel.grid(row=2,column=0)
    videoloop2()
    ventana2.update()

def video3():
    v3 = cv2.VideoCapture('3.mp4')
    current_image = None
    def videoloop3():
        ventana2.update()
        ok, frame = v3.read()  
        if ok:  
            key = cv2.waitKey(1)
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            current_image = Image.fromarray(cv2image)  
            imgtk = ImageTk.PhotoImage(image=current_image)   
            panel.imgtk = imgtk    
            panel.config(image=imgtk)  
        ventana2.after(1,videoloop3)
    panel = Label(ventana2)
    ventana2.columnconfigure(0,weight=1)
    panel.grid(row=2,column=0)
    videoloop3()
    ventana2.update()

def video4():
    v4 = cv2.VideoCapture('4.mp4')
    current_image = None
    def videoloop4():
        ventana2.update()
        ok, frame = v4.read()  
        if ok:  
            key = cv2.waitKey(1)
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            current_image = Image.fromarray(cv2image)  
            imgtk = ImageTk.PhotoImage(image=current_image)   
            panel.imgtk = imgtk    
            panel.config(image=imgtk)  
        ventana2.after(1,videoloop4)
    panel = Label(ventana2)
    ventana2.columnconfigure(0,weight=1)
    panel.grid(row=2,column=0)
    videoloop4()
    ventana2.update()

def video5():
    v5 = cv2.VideoCapture('5.mp4')
    current_image = None
    def videoloop5():
        ventana2.update()
        ok, frame = v5.read()  
        if ok:  
            key = cv2.waitKey(1)
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            current_image = Image.fromarray(cv2image)  
            imgtk = ImageTk.PhotoImage(image=current_image)   
            panel.imgtk = imgtk    
            panel.config(image=imgtk)  
        ventana2.after(1,videoloop5)
    panel = Label(ventana2)
    ventana2.columnconfigure(0,weight=1)
    panel.grid(row=2,column=0)
    videoloop5()
    ventana2.update()

def video6():
    v6 = cv2.VideoCapture('6.mp4')
    current_image = None
    def videoloop6():
        ventana2.update()
        ok, frame = v6.read()  
        if ok:  
            key = cv2.waitKey(1)
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            current_image = Image.fromarray(cv2image)  
            imgtk = ImageTk.PhotoImage(image=current_image)   
            panel.imgtk = imgtk    
            panel.config(image=imgtk)  
        ventana2.after(1,videoloop6)
    panel = Label(ventana2)
    ventana2.columnconfigure(0,weight=1)
    panel.grid(row=2,column=0)
    videoloop6()
    ventana2.update()

def video7():
    v7 = cv2.VideoCapture('7.mp4')
    current_image = None
    def videoloop7():
        ventana2.update()
        ok, frame = v7.read()  
        if ok:  
            key = cv2.waitKey(1)
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            current_image = Image.fromarray(cv2image)  
            imgtk = ImageTk.PhotoImage(image=current_image)   
            panel.imgtk = imgtk    
            panel.config(image=imgtk)  
        ventana2.after(1,videoloop7)
    panel = Label(ventana2)
    ventana2.columnconfigure(0,weight=1)
    panel.grid(row=2,column=0)
    videoloop7()
    ventana2.update()

def video8():
    v8 = cv2.VideoCapture('8.mp4')
    current_image = None
    def videoloop8():
        ventana2.update()
        ok, frame = v8.read()  
        if ok:  
            key = cv2.waitKey(1)
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            current_image = Image.fromarray(cv2image)  
            imgtk = ImageTk.PhotoImage(image=current_image)   
            panel.imgtk = imgtk    
            panel.config(image=imgtk)  
        ventana2.after(1,videoloop8)
    panel = Label(ventana2)
    ventana2.columnconfigure(0,weight=1)
    panel.grid(row=2,column=0)
    videoloop8()
    ventana2.update()
    
def video9():
    v9 = cv2.VideoCapture('9.mp4')
    current_image = None
    def videoloop9():
        ventana2.update()
        ok, frame = v9.read()  
        if ok:  
            key = cv2.waitKey(1)
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            current_image = Image.fromarray(cv2image)  
            imgtk = ImageTk.PhotoImage(image=current_image)   
            panel.imgtk = imgtk    
            panel.config(image=imgtk)  
        ventana2.after(1,videoloop9)
    panel = Label(ventana2)
    ventana2.columnconfigure(0,weight=1)
    panel.grid(row=2,column=0)
    videoloop00()
    ventana2.update()
    
def video10():
    v10 = cv2.VideoCapture('10.mp4')
    current_image = None
    def videoloop10():
        ventana2.update()
        ok, frame = v10.read()  
        if ok:  
            key = cv2.waitKey(1)
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            current_image = Image.fromarray(cv2image)  
            imgtk = ImageTk.PhotoImage(image=current_image)   
            panel.imgtk = imgtk    
            panel.config(image=imgtk)  
        ventana2.after(1,videoloop10)
    panel = Label(ventana2)
    ventana2.columnconfigure(0,weight=1)
    panel.grid(row=2,column=0)
    videoloop10()
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
    ventana2.columnconfigure(0,weight=1)
    panel.grid(row=2,column=0)
    videoloop00()
    ventana2.update()
    
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
    ventana2.columnconfigure(0,weight=1)
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
        ventana2.columnconfigure(0,weight=1)
        Labeli.grid(row=2,column=0)
        ventana2.update()
        Labelt.config(text='Cumplió con el tiempo requerido')
        ventana2.update()
##        cur.execute("INSERT INTO manitor VALUES(nextval('usuario_sequence'), now(), 'cumplio con el tiempo en jabon')")
##        Labeli.config(image=img0)
##        Labeli.image=img0()
        time.sleep(2)
        return True
        
        
    elif auxVariable == 2:
        Labeli=Label(ventana2,image=imgF)
        ventana2.columnconfigure(0,weight=1)
        Labeli.grid(row=2,column=0)
        ventana2.update()
        Labelt.config(text="No se detectó movimiento de sus manos \n Vuelva a empezar")
##        cur.execute("INSERT INTO manitor VALUES(nextval('usuario_sequence'), now(), 'No hubo suficiente movimiento de las manos')")
        ventana2.update()
        time.sleep(2)
        return False

        
    elif auxVariable == 3:
        Labeli=Label(ventana2,image=imgF)
        ventana2.columnconfigure(0,weight=1)
        Labeli.grid(row=2,column=0)
        ventana2.update()
        Labelt.config(text="No se detectaron sus manos \n Vuelva a empezar")
##        cur.execute("INSERT INTO manitor VALUES(nextval('usuario_sequence'), now(), 'No se detectaron las manos')")
        ventana2.update()
        time.sleep(2)
        return False
        

    elif auxVariable == 4:
        Labeli=Label(ventana2,image=imgF)
        ventana2.columnconfigure(0,weight=1)
        Labeli.grid(row=2,column=0)
        ventana2.update()
        Labelt.config(text="No se detectaron sus manos dentro de la región de lectura \n Vuelva a empezar")
##        cur.execute("INSERT INTO manitor VALUES(nextval('usuario_sequence'), now(), ' No se registraron manos dentro de la region')")
        ventana2.update()
        time.sleep(2)
        return False      

######################## ....................... #######################

def inicio(c):
    global ventana2, Labeli, Labelt, panel
    global img0, img1, imgF
    img0=PhotoImage(file="00.gif") # Reads photos
    img1=PhotoImage(file="11.gif")
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
        
        Labeli=Label(ventana2,image=img1) # ventana2 IMAGEN
        ventana2.columnconfigure(0,weight=1)
        ventana2.update()
        Labeli.grid(row=2,column=0)
        
    else:#Toda esta parte no es necesaria se podria borrar hasta el update, ya que es un estado inical que nunca se muestra igual que arriba
        Labelt.config(text='BIENVENIDO ')
        ventana2.update()
        Labeli=Label(ventana2,image=img1)
        ventana2.columnconfigure(0,weight=1)
        Labeli.grid(row=2,column=0)
        Labeli.config(image=img1)
        Labeli.image=img1
        ventana2.update()
    ventana.iconify() # Turns window into an icon

    while 1:

##        cur.execute("INSERT INTO manitor VALUES(nextval('usuario_sequence'), current_timestamp, ' inicio ')")
        Labeli.destroy()
        ventana2.update()
        Labelt.config(text='BIENVENIDO \n  Por favor moje sus manos con agua')
        ventana2.update()
        video000                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     ()
        ventana2.update()
        
        Labelt.config(text='Deposite jabón en la mano')
##        cur.execute("INSERT INTO manitor VALUES(nextval('usuario_sequence'), current_timestamp, ' nuevo usuario ')")
        ventana2.update()

        def cero():
            b,auxType = contadorMovimiento.funcionMovimientoEnRegion(y[1],3,2,lower,upper) 
            instruction = falseType(b,auxType,Labelt,Labeli,img0,imgF)
            if not instruction:
                inicio(0)
                
        Thread(target=cero).start()
        Thread(target=video00()).start()

######################## instruccion 1
        
        Labeli.destroy()
        Labelt.config(text='Frote las palmas de las manos \n entre sí')
        ventana2.update()

        def primero():
            d,auxType = contadorMovimiento.funcionMovimientoEnRegion(y[1],3,2,lower,upper) 
            instruction = falseType(d,auxType,Labelt,Labeli,img0,imgF)
            if not instruction:
                inicio(0)
                
        Thread(target=primero).start()
        Thread(target=video1()).start()

########################## instruccion2
##
##        Labeli.destroy()
##        Labelt.config(text='Frote la palma de la mano derecha \n contra el dorso de la mano izquierda  \n entrelazando los dedos y viceversa')
##        panel = Label(ventana2)

##        def segundo():
##            e,auxType = contadorMovimiento.funcionMovimientoEnRegion(y[1],10,2,lower,upper) 
##            instruction = falseType(e,auxType,Labelt,Labeli,img0,imgF)
##            if not instruction:
##                inicio(0)
##                
##        Thread(target=segundo).start()
##        Thread(target=video1()).start()
##        
##        time.sleep(10)

######################## fin instrucciones
##
        Labeli=Label(ventana2,image=img12)
        ventana2.columnconfigure(0,weight=1)
        Labeli.grid(row=2,column=0)
        ventana2.update()
        Labelt.config(text='Sus manos son seguras')
##        Labeli.config(image=img12)
##        Labeli.image=img12
        ventana2.update()
        time.sleep(5)

######################## ........................ ######################  

inicio_arg=partial(inicio,1)
botoninicio = Button(ventana,text="INICIAR",fg="white",command=inicio_arg,
                     bg='red',font=("Helvetica 12 bold"))
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
        print 'i'

botonbase = Button(ventana,text="BASEDATOS",fg="white",command=basesita,
                     bg='red',font=("Helvetica 12 bold"))
botonbase.grid(row=9,column=1)

######################## LABEL FIN + FUNC FIN + BOTON FIN 

labelfin=Label(ventana,
             text="si desea finalizar",
             fg="black",bg="white",font=("Helvetica 12 "))
labelfin.grid(row=10,column=1)

def finalizar():
    ventana.destroy()

botonfin = Button(ventana,text="FIN",fg="white",command=finalizar,
                     bg='red',font=("Helvetica 12 bold"))
botonfin.grid(row=11,column=1)

######################################################################

ventana.mainloop()
