import sys,pygame 
import Image 
from sys import argv 
import numpy

def main():
    image,ancho,alto,matriz= escala_grises(argv[1])
    image_filtro = filtro(image,ancho,alto,matriz)
    ventana = pygame.display.set_mode((ancho,alto)) 
    pygame.display.set_caption('Imagen')  
    imagen = pygame.image.load(image_filtro) 
    while True: 
        for eventos in pygame.event.get():
            if eventos.type == pygame.QUIT:
                sys.exit(0)
        ventana.blit(imagen,(0,0))
        pygame.display.update()
    return 0

def filtro(image,ancho,alto,matriz):
    new_image = 'filtro.png'
    pixels = image.load()
    lista = [-1,0,1]
    for i in range(ancho):
        for j in range(alto):
            promedio = vecindad(i,j,lista,matriz)
            pixels[i,j] = (promedio,promedio,promedio)
    image_filtro = image.save(new_image)
    return new_image

def vecindad(i,j,lista,matriz):
    promedio = 0
    indice  = 0
    for x in lista:
        for y in lista:
            a = i+x
            b = j+y
            try:
                if matriz[a,b]:
                    promedio += matriz[a,b] 
                    indice +=1            
            except IndexError:
                pass
    try:
        promedio=int(promedio/indice)
        return promedio
    except ZeroDivisionError:
        return 0
    
def escala_grises(image):
    image = Image.open(image)
    new_image = 'escala_grises.png'
    pixels = image.load()
    ancho,alto = image.size
    matriz = numpy.empty((ancho, alto))
    for i in range(ancho):
        for j in range(alto):
            (r,g,b) = image.getpixel((i,j))
            escala = (r+g+b)/3
            pixels[i,j] = (escala,escala,escala)
            matriz[i,j] = int(escala)
    image_filtro = image.copy()

    image = image.save(new_image)
    return image_filtro,ancho,alto,matriz
           
main()
