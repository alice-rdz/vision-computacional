import sys,pygame #Importar para la creacion de la vetana
import Image #Importar para trabajar con imagene (PIL)
from sys import argv #Importar para trabajar con argumentos de terminal

#def main: se crea la ventana y se carga la imagen ya en escala de grises

def main(image):
    ancho,altura,new_image=escala_grises(image) #Llama a funcion escala de grises

    ventana = pygame.display.set_mode((ancho,altura)) #Crea una ventana cn las dimensiones de la imagen
    pygame.display.set_caption('Imagen') #Definimos el nombre d ela ventana 
    imagen = pygame.image.load(new_image) #Carga nuestra imagen 
    while True: #Para que la ventana no se cierre
        #Para poder cerrar la ventana
        for eventos in pygame.event.get():
            if eventos.type == pygame.QUIT:
                sys.exit(0)
        ventana.blit(imagen,(0,0))#Mostrar la imagen posicion x=0, y=0
        pygame.display.update()
    return 0

#Convierte la imagen a escalade grises
def escala_grises(image):
    image = Image.open(image)
    new_image = 'escala_grises.png' 
    pixeles = image.load()
    ancho, altura =image.size
    for i in range(ancho):
        for j in range(altura):
            (r,g,b) = image.getpixel((i,j))
            escala = (r+g+b)/3
            pixeles[i,j]=(escala,escala,escala)
    
    image=image.save(new_image)
    return ancho,altura,new_image

pygame.init() #Inicializa pygame
main(argv[1])
