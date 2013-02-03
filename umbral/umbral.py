import sys,pygame
import Image 
from sys import argv

def main(image):
    ancho,altura,new_image=umbral(image)
    ventana = pygame.display.set_mode((ancho,altura)) 
    pygame.display.set_caption('Imagen') 
    imagen = pygame.image.load(new_image) 
    while True: 
        
        for eventos in pygame.event.get():
            if eventos.type == pygame.QUIT:
                sys.exit(0)
        ventana.blit(imagen,(0,0))
        pygame.display.update()
    return 0


def umbral(image):
    minimo = int(argv[2])
    maximo = int(argv[3])
    image = Image.open(image)
    new_image = 'umbral.png' 
    pixeles = image.load()
    ancho, altura =image.size
    print ancho
    print altura
    for i in range(ancho):
        for j in range(altura):
            (r,g,b) = image.getpixel((i,j))
            promedio = int((r+g+b)/3)
            if promedio <= minimo:
                promedio = 0
            if promedio >= maximo:
                promedio = 255
            pixeles[i,j]=(promedio,promedio,promedio)
    image=image.save(new_image)
    return ancho,altura,new_image

pygame.init() 
main(argv[1])
