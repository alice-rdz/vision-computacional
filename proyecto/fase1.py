from Tkinter import *
import Image,ImageTk
import ImageDraw
from sys import argv
from time import * 
import numpy
from math import floor
import math
import random
class Aplicacion(Frame):
    def __init__(self,parent):
        Frame.__init__(self,parent)
        
        self.parent = parent
        self.initUI()
   
    def initUI(self):
        self.parent.title('Ventana')
        self.pack(fill=BOTH, expand=1)
        self.o_imagen=argv[1]
        imagen = self.obtener_imagen()
        self.cargar_imagen(imagen)
        self.conv = Button(text='POLIGONOS', command =self.boton_c).pack(side=LEFT)
   #     self.colors = Button(text='Colorear', command =self.boton_colorear).pack(side=LEFT)
        
    def boton_c(self):
        image = self.filtro()
        img = self.mascara(image)
        masa,imagen=self.formas()
        #pendientes=self.get_pendientes(img)
        #self.get_rectas(pendientes,img)
        #masa=self.formas()
        self.obtener_lineas(masa,imagen)
        #self.detectar_rectas(img,masa,pendientes)
        
    def obtener_lineas(self,poligonos,imagen):
        poligonos.pop(0)
        rectangulos=[]
        for poligono in poligonos:
            pendientes,med=self.get_pendientes(poligono,imagen)
            print 'regreso de obtener pendientes'
            imagen,segmentos=self.get_rectas(pendientes,imagen,poligono,med)
            num=len(segmentos)
        #    if num==4:
        #        v,rec=self.detectar(segmentos)
       #         if v=True:
      #              rectangulos.append(rec)
            #self.puntos_medios(segmentos)

    #def detectar(self,segmentos):
        #Aqui detecta si el poligono realmente es un rectangulo y no un cuadrado
        

    def puntos_medios(self,segmentos):
        for line in segmentos:
            px1,py1=line[0]
            px2,py2=line[-1]
            pm=((px1+px2)/2,(py1+py2)/2)
            
            
            

    def boton_convolucion(self):
        image = self.filtro()
        ima=image.save('filtrada.jpg')
        img = self.mascara(image)
        id = img.save('mascara.png')
        img=self.normalizar(img)
        img2 = img.save('normalizada.png')
        im_bin = self.binarizar(img)
        imbin=img.save('binarizada.png')
        img = self.cargar_imagen(im_bin)
        return im_bin

    def formas(self):
        imagen,masa=self.c_colorear()
        return masa,imagen

    def c_colorear(self):
        img=self.boton_convolucion()
        pixels=img.load()
        porcentajes=[]
        fondos=[]
        centro_masa=[]
        masa=[]
        ancho,alto=img.size
        t_pixels=ancho*alto
        c=0
        pintar=[]
        f=0
        m=[]
        for i in range(ancho):
            for j in range(alto):
                pix = pixels[i,j]
                r,g,b= random.randint(0,255),random.randint(0,255), random.randint(0,255)
                fondo=(r,g,b)
                if (pix==(255,255,255)):
                    c +=1
                    origen=(i,j)
                    num_pixels,abscisa,ordenada,puntos=self.bfs(pix,origen,img,fondo)
                    p=(num_pixels/float(t_pixels))*100
                    if p>.10:
                        centro=(sum(abscisa)/float(num_pixels),sum(ordenada)/float(num_pixels))
                        centro_masa.append(centro)
                        masa.append(num_pixels)
                        porcentajes.append(p)
                        fondos.append(fondo)
                        m.append(puntos)
                        centro_masa.append(centro)
        img.save('final.jpg')
        return img,m

    def centro_masa(self,im,centros):
        draw = ImageDraw.Draw(im)
        for i,punto in enumerate(centros):
            draw.ellipse((punto[0]-2, punto[1]-2, punto[0]+2, punto[1]+2), fill=(0,0,0))
            label_id = Label(text=i)
            label_id.place(x = punto[0]+16,  y = punto[1])
        im.save('centro.png')
        return
 
    def imprimir_porcentajes(self,porcentajes):
        for i,p in enumerate(porcentajes):
            print 'Figura ID: %d  Porcentaje: %f' %(i,p)


    def bfs(self,pix,origen,im,fondo):
        pixels=im.load()
        cola=list()
        lista=[-1,0,1]
        abscisa=[]
        ordenada=[]
        puntos=[]
        cola.append(origen)
        original = pixels[origen]
        num=1
        while len(cola) > 0:
            (i,j)=cola.pop(0)
            actual = pixels[i,j]
            if actual == original or actual==fondo:
                for x in lista:
                    for y in lista:
                        a= i+x
                        b = j+y 
                        try:
                            if pixels[a,b]:
                                contenido = pixels[a,b]
                                if contenido == original:
                                    pixels[a,b] = fondo
                                    abscisa.append(a)
                                    ordenada.append(b)
                                    num +=1
                                    cola.append((a,b))
                                    puntos.append((a,b))
                        except IndexError:
                            pass
        im.save('23333.png')
        return num,abscisa,ordenada,puntos
    
    def get_rectas(self,pendientes,img,poligono,med):
        segmentos=list()
        pixels=img.load()
        ancho,alto=img.size
        for m in med:
            linea=[]
            r,g,b= random.randint(0,255),random.randint(0,255), random.randint(0,255)
            fondo=(r,g,b)
            for p in poligono:
                i,j=p
                if pendientes[i,j]==m:
                    pixels[i,j]=fondo
                    linea.append((i,j))
            if len(linea)>15:
                segmentos.append(linea)
        img.save('i.png')
        return img,segmentos
    
    def get_pendientes(self,puntos,imagen):
        Gx=self.gx
        Gy=self.gy
        pixels=imagen.load()
        ancho,alto=imagen.size
        pendientes=numpy.empty((ancho, alto))
        med=[]
        for p in puntos:
            i,j=p
            if Gx[i,j]<0 and Gy[i,j]>0:
                m=0
            elif Gx[i,j]>0 and Gy[i,j]<0:
                m=1
            elif Gy[i,j]<=0 and Gx[i,j]==0:
                m=2
            elif Gy[i,j]>=0 and Gx[i,j]==0:
                m=3
            elif Gx[i,j]<=0 and Gy[i,j]==0:
                m=4
            elif Gx[i,j]>=0 and Gy[i,j]==0:
                m=5
            elif Gx[i,j]<0 and Gy[i,j]<0:
                m=6
            elif Gy[i,j]>0 and Gx[i,j]>0:
                m=7
            if m not in med:
                med.append(m)
            pendientes[i,j]=m

        print 'termino'
        print 'pendientes',pendientes
        return pendientes,med
   
    def filtro(self):
        inicio = time()
        image = self.escala_grises()
        pixels = image.load()
        ancho, alto =image.size
        lista = [-1,0,1]
        for i in range(ancho):
            for j in range(alto):
                promedio = self.vecindad(i,j,lista,self.matriz)
                pixels[i,j] = (promedio,promedio,promedio)
        fin = time()
        tiempo_t = fin - inicio
        #print "Tiempo que tardo en ejecutarse filtro = "+str(tiempo_t)+" segundos"
        return image

    def escala_grises(self):
        inicio = time()
        image = Image.open(self.o_imagen) 
        pixels = image.load()
        ancho,alto = image.size
        self.matriz = numpy.empty((ancho, alto))
        for i in range(ancho):
            for j in range(alto):
                (r,g,b) = image.getpixel((i,j))
                escala = (r+g+b)/3
                pixels[i,j] = (escala,escala,escala)
                self.matriz[i,j] = int(escala)
        fin = time()
        tiempo_t = fin - inicio
       # print "Tiempo que tardo en ejecutarse escala de grises = "+str(tiempo_t)+" segundos"
        df = image.save('escala.png')
        return image 

    
    def vecindad(self,i,j,lista,matriz):
        promedio = 0
        indice  = 0
        for x in lista:
            for y in lista:
                a = i+x
                b = j+y
                try:
                    if self.matriz[a,b] and (x!=a and y!=b):
                        promedio += self.matriz[a,b] 
                        indice +=1            
                except IndexError:
                    pass
            try:
                promedio=int(promedio/indice)
                return promedio
            except ZeroDivisionError:
                return 0
  

    def mascara(self,image):
        inicio = time()
        #Mascara Sobel
        sobelx = ([-1,0,1],[-2,0,2],[-1,0,1]) #gradiente horizontal
        sobely = ([1,2,1],[0,0,0],[-1,-2,-1]) # gradiente vertical    
        img=self.convolucion(sobelx,sobely,image)
        fin=time()
        tiempo_t = fin - inicio
        #print "Tiempo que tardo en ejecutarse convolucion = "+str(tiempo_t)+" segundos"

        return img
    
    def convolucion(self,h1,h2,image):
        pixels = image.load()
        ancho,alto = image.size 
        a=len(h1[0])
        self.conv = numpy.empty((ancho, alto))
        self.gx=numpy.empty((ancho, alto))
        self.gy=numpy.empty((ancho, alto))
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
                self.gx[x,y]=sumax
                self.gy[x,y]=sumay
                gradiente = int(gradiente)
                pixels[x,y] = (gradiente,gradiente,gradiente)
                p = gradiente
                if p < self.minimo:
                    self.minimo = p
                if  p > self.maximo:
                    self.maximo = p
       # print 'gx-------------',self.gx
       # print 'gy-------------',self.gy
        return image

    def normalizar(self,image):
        inicio=time()
        pixels = image.load()
        r = self.maximo-self.minimo
        prop = 255.0/r
        ancho,alto = image.size
        for i in range(ancho):
            for j in range(alto):
                p =int(floor((self.conv[i,j]-self.minimo)*prop))
                pixels[i,j]=(p,p,p);
       # print 'TERMINO'
        fin = time()
        tiempo_t = fin - inicio
       # print "Tiempo que tardo en ejecutarse normalizar = "+str(tiempo_t)+" segundos"

        return image


    def binarizar(self,img):
        inicio = time()
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
        fin  =time()
        tiempo_t = fin - inicio
       # print "Tiempo que tardo en ejecutarse binzarizar = "+str(tiempo_t)+" segundos"

        return img
    
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
