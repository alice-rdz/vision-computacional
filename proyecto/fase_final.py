from Tkinter import *
import Image
import ImageDraw,ImageTk
from sys import argv
from time import * 
import numpy
import MySQLdb #Modulo para trabajar con mysql
from numpy import array
import PIL
from squares import *
#from PIL import ImageTk
from math import floor
import math
import random
import matplotlib.pyplot as plt

tiempos =[]

class Aplicacion(Frame):
    def __init__(self,parent):
        Frame.__init__(self,parent)
        self.parent = parent
        self.initUI()
   
    def initUI(self):
        self.parent.title('Ventana')
        self.parent.geometry("300x300")
        self.pack(fill=BOTH, expand=1)
        self.o_imagen=argv[1]
        imagen = self.obtener_imagen()
        self.cargar_imagen(imagen)
        self.detect= Button(text='Deteccion', command =self.boton_deteccion).pack(side=LEFT)

    def boton_deteccion(self):
        global tiempos
        print 'Detectando cuadrado...'
        inicio_c=time()
        inicio=time()
        squares = busqueda(self.o_imagen)
       # self.dibujar(squares,self.o_imagen)
        print 'Termino deteccion de cuadrado'
        fin_c=time()
        tiempo_t = fin_c - inicio_c
        tiempos.append(tiempo_t)
        print "Tiempo que tardo en ejecutarse la deteccion del cuadrado = "+str(tiempo_t)+" segundos"
        inicio_r=time()
        img=self.cortar(self.o_imagen,squares)
        fin_r=time()
        tiempo_r = fin_r - inicio_r
        tiempos.append(tiempo_r)
        img_c=img.copy() 
        imagen_grises=self.escala_grises(img)                                                                                                 
        imagen_filtro=self.filtro(imagen_grises)                                                                                               
        imagen_conv=self.mascara(imagen_filtro)                                                                                               
        imagen_nor=self.normalizar(imagen_conv)                                                                                                
        imagen_binarizar=self.binarizar(imagen_nor)                                                                                           
        form,num=self.formas(imagen_binarizar)
        form.pop(0)
        datos=self.deteccion_color(img_c,form)
        self.conexion(datos,num-1)
       # print 'iniciar',len(form)
       # form.pop(0)
      #  print 'len formas ',len(form)
        fin=time()
        tiempo_t = fin - inicio
        print 'tiempos',tiempos
        #self.graficar(tiempos)
        print "Tiempo total para la deteccion = "+str(tiempo_t)+" segundos"
        print 'termino'
        return


    def graficar(self,timers):
        plt.clf()
        fig=plt.subplot(111)
        tope=max(timers)
        minx=min(timers)
        topey=len(timers)
        miny=('rectangle','escala','filtro','mascara','normalizacion','binarizacion','formas')
       # ancho,alto=image.size
        plt.ylim(-1,7)
        plt.xlim(minx,tope)
        plt.title('Vision')
        x=range(1,7)
        plt.plot(x,timers,'r-',linewidth=2,label='horizontal')
        #plt.plot(y,vertical,'b-',linewidth=2,label='vertical')
        box = fig.get_position()
        fig.set_position([box.x0, box.y0 + box.height * 0.1,box.width, box.height * 0.9])
        fig.legend(loc = 'upper center', bbox_to_anchor=(0.5, -0.05),
                   fancybox = True, shadow = True, ncol = 1)
        plt.show()
        return

    def conexion(self,datos,num):
       # print 'datos',datos
       # print 'entro a conexion'
        host = "localhost"
        user = "root"
        passwd = "alice"
        db = "vision"
        data_base = MySQLdb.connect(host, user,passwd,db) #Conxion a la base de datos                  
        cursor = data_base.cursor()
        consulta='SELECT `id`,`nombre` FROM `pinturas` where `c_formas`= "%d"' % (num)
        cursor.execute(consulta)
        ob=cursor.fetchall()
        for row in ob:
            id_p=row[0]
            nombre_p=row[1]
            validar=False
            c =1
            for dat in datos:
                priori=c
                consulta2='SELECT * FROM `caracteristicas` where `id_pintura`="%d" and `prioridad`="%d"'%(id_p,priori)
                cursor.execute(consulta2)
                ob2=cursor.fetchall()
                c +=1
               # print 'ob2 r',ob2[0][1]
               # print 'ob2 g',ob2[0][2]
               # print 'ob3 b',ob2[0][3]
               # print 'priori',priori
               # print dat[0][0]
               # print dat[0][1]
               # print dat[0][2]
                if((ob2[0][1]-10<=dat[0][0]<=ob2[0][1]+10)and (ob2[0][2]-10<= dat[0][1] <=ob2[0][2]+10) and (ob2[0][3]-10<= dat[0][2] <=ob2[0][3]+10)):
                 #   print 'entro a if'
                    validar= True
                else:
                    validar=False
            if (validar):
                print "la pintura es:"+nombre_p
                break;
            #else:
            #    print 'No se encontro coincidencia'
        #print "la pintura es:"+nombre_p

              #  for row2 in ob2:
                    
                

        return

    def deteccion_color(self,img,formas):
        datos=[]
        global tiempos
        inicio=time()
        for i,j in enumerate(formas):
          #  print i
            color=self.get_color(j,img)
            datos.append((color,i+1))
        fin=time()
        tiempo_t = fin - inicio
        tiempos.append(tiempo_t)
       # print datos
        return datos

    def get_color(self,puntos,img):
        img.save('CHECAR.png')
        valor_r=0
        valor_g=0
        valor_b=0
        p_r=0
        p_g=0
        p_b=0
        n=len(puntos)
        pixels=img.load()
        for i in puntos:
            r,g,b=pixels[i]
            valor_r +=r
            valor_g +=g
            valor_b +=b
        p_r=(valor_r/n)
        p_g=(valor_g/n)
        p_b=(valor_b/n)
        return (p_r,p_g,p_b)
            
            
    def dibujar(self,square,img):
        img=Image.open(img)
        p1=square[0]
        p2=square[1]
        p3=square[2]
        p4=square[3]
        m1=(p1[0]+p3[0])/2
        m2=(p1[0]+p3[0])/2
        p_m=(int(m1),int(m2))
        draw= ImageDraw.Draw(img)
 #       draw.rectangle(((p4[0], p4[1]), (p4[0]-p1[0],p2[0]-p1[0])), outline=(0,255,255))
        #print p1
        draw.rectangle(((p4[0], p4[1]),(30,20)),outline=(0,255,255))

               #draw.point(p_m,fill=(0,0,255))
        draw.ellipse((p1[0]-2, p1[1]-2, p1[0]+2, p1[1]+2), fill=(0,0,0))
        draw.ellipse((p2[0]-2, p2[1]-2, p2[0]+2, p2[1]+2), fill=(0,0,0))
        draw.ellipse((p3[0]-2, p3[1]-2, p3[0]+2, p3[1]+2), fill=(255,0,0))
        #draw.polygon([(p1[0],p1[1]), (p2[0],p2[1]), (p3[0],p3[1]),(p4[0],p4[1])], outline=(0,0,255))
        img.save('punto.png')

    def cortar(self,image,square):
        image=Image.open(image)
        ancho,alto = image.size
        p1=square[0]
        p2=square[1]
        p3=square[2]
        p4=square[3]
        puntos=list()
        pixels = image.load()
        an=(p4[0]-p1[0])+1
        al=(p2[1]-p1[1])+1
        im = Image.new('RGB', (an, al), (255, 255, 255))
        im.save('nueva.png')
        pix=im.load()
        for i in range(ancho):
            if i>=p1[0] and i<=p4[0]:
                for j in range(alto):
                    if j>=p1[1] and j<=p2[1]:
                        puntos.append((i,j))
        c=0
        image.save('please.png')
        for i in range(an):
            for j in range(al):
                pix[i,j]=pixels[puntos[c]]
                c +=1
        im.save('despues.png')
        return im

    def normalizar(self,image):
        global tiempos
        inicio=time()
        pixels = image.load()
        r = self.maximo-self.minimo
        prop = 255.0/r
        ancho,alto = image.size
        for i in range(ancho):
            for j in range(alto):
                if pixels[i,j][0]!=0:
                    p =int(floor((pixels[i,j][0]-self.minimo)*prop))
                    pixels[i,j]=(p,p,p)
        fin = time()
        tiempo_t = fin - inicio
        tiempos.append(tiempo_t)
        print "Tiempo que tardo en ejecutarse Normalizar = "+str(tiempo_t)+" segundos"
        image.save('Normaliza.png')

        return image

    def binarizar(self,img):
        global tiempos
        inicio=time()
        pixels = img.load()
        ancho,alto = img.size
        minimo = int(argv[2])
        for i in range(ancho):
            for j in range(alto):
                if pixels[i,j][1] < minimo:
                    p=0
                else:
                    p= 255
                pixels[i,j]=(p,p,p)
        fin = time()
        tiempo_t = fin - inicio
        tiempos.append(tiempo_t)
        print "Tiempo que tardo en ejecutarse binarizar = "+str(tiempo_t)+" segundos"
        img.save('Binarizar.png')                                                         
        return img


    def filtro(self,image):
        global tiempos
        inicio = time()
        pixels = image.load()
        ancho, alto =image.size
        lista = [-1,0,1]
        for i in range(ancho):
            for j in range(alto):
                promedio = self.vecindad(i,j,lista,pixels)
                pixels[i,j] = (promedio,promedio,promedio)
        fin = time()
        tiempo_t = fin - inicio
        tiempos.append(tiempo_t)
        print "Tiempo que tardo en ejecutarse filtro = "+str(tiempo_t)+" segundos"
        image.save('Filtro.png')
        return image

    def vecindad(self,i,j,lista,matriz):
        promedio = 0
        indice  = 0
        for x in lista:
            for y in lista:
                a = i+x
                b = j+y
                try:
                    if matriz[a,b] and (x!=a and y!=b):
                        promedio += matriz[a,b][0] 
                        indice +=1            
                except IndexError:
                    pass
        try:
            promedio=int(promedio/indice)
            return promedio
        except ZeroDivisionError:
            return 0


    def escala_grises(self,image):
        global tiempos
        inicio = time()
        #image = Image.open(img)
        pixels = image.load()
        ancho,alto = image.size
        #print puntos
        #print 'entro a grises'
        for i in range(ancho):
            for j in range(alto): 
               # print i,j
               # if (i,j) in puntos:
               # print 'entro'
                (r,g,b) = image.getpixel((i,j))
                escala = (r+g+b)/3
                pixels[i,j] = (escala,escala,escala)
        fin = time()
        tiempo_t = fin - inicio
        df = image.save('escala.png')
        tiempos.append(tiempo_t)
        print 'Tiempo escala de grises: ',tiempo_t
        return image
    

    def bfs(self,pix,origen,im,fondo):
        pixels=im.load()
        cola=list()
        lista=[-1,0,1]
        cola.append(origen)
        original = pixels[origen]
        num=1
        puntos=[]
        while len(cola) > 0:
            (i,j)=cola.pop(0)
            actual = pixels[i,j]
            if actual == original or actual==fondo:
              #  pixels[i,j] = fondo
                for x in lista:
                    for y in lista:
                        a= i+x
                        b = j+y 
                        try:
                            if pixels[a,b]:
                                contenido = pixels[a,b]
                                if contenido == original:
                                    pixels[a,b] = fondo
                                    puntos.append((a,b))
                                    num +=1
                                    cola.append((a,b))
                        except IndexError:
                            pass
        im.save('23333.png')
        return num,puntos

    def formas(self,im):
        global tiempos
        inicio = time()
        pixels=im.load()
        ancho,alto=im.size
        t_pixels=ancho*alto
        num=0
        form=[]
        for i in range(ancho):
            for j in range(alto):
                pix = pixels[i,j]
                r,g,b= random.randint(0,255),random.randint(0,255), random.randint(0,255)
                fondo=(r,g,b)
                if (pix==(0,0,0)):
                    origen=(i,j)
                    num_pixels,puntos=self.bfs(pix,origen,im,fondo)
                    p=(num_pixels/float(t_pixels))*100
                    if p>1:
                        form.append(puntos)
                        num +=1
                        #marcar(puntos)
        im.save('Formas.png')
        fin=time()
        tiempo_t = fin - inicio
        tiempos.append(tiempo_t)
        return form,num

    #def comprobar(self,puntos):
        


    def mascara(self,image):
        global tiempos
        inicio = time()
        #Mascara Sobel
        sobelx = ([-1,0,1],[-2,0,2],[-1,0,1]) #gradiente horizontal
        sobely = ([1,2,1],[0,0,0],[-1,-2,-1]) # gradiente vertical    
        img=self.convolucion(sobelx,sobely,image)
        fin=time()
        tiempo_t = fin - inicio
        tiempos.append(tiempo_t)
        image.save('convolucion.png')
        print "Tiempo que tardo en ejecutarse convolucion = "+str(tiempo_t)+" segundos"
        return img
    
    def convolucion(self,h1,h2,image):
        pixels = image.load()
        ancho,alto = image.size 
        a=len(h1[0])
        self.conv = numpy.empty((ancho, alto))
        self.minimo = 255
        self.maximo = 0
        for x in range(ancho):
            for y in range(alto):
                sumax = 0.0
                sumay = 0.0
                for i in range(a): 
                    for j in range(a): 
                        try:
                            sumax +=(pixels[x+i,y+j][0]*h1[i][j])
                            sumay +=(pixels[x+i,y+j][0]*h2[i][j])

                        except:
                            pass
                gradiente = math.sqrt(pow(sumax,2)+pow(sumay,2))
                self.conv[x,y]=gradiente
                gradiente = int(gradiente)
                pixels[x,y] = (gradiente,gradiente,gradiente)
                p = gradiente
                if p < self.minimo:
                    self.minimo = p
                if  p > self.maximo:
                    self.maximo = p
        return image

    def obtener_imagen(self):
        imagen = Image.open(self.o_imagen)
        imagen = imagen.convert('RGB')
        return imagen


    def cargar_imagen(self,imagen):
        img = ImageTk.PhotoImage(imagen) 
        label = Label(self, image=img)
        label.imagen = img
        label.place(x=10, y=10)

def main():
    root = Tk()
    app = Aplicacion(root)
    root.mainloop()
    
main()
