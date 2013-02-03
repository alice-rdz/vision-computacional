import sys,pygame
import Image 
from sys import argv 

def main(image):
    ventana = pygame.display.set_mode((300,300)) 
    pygame.display.set_caption('Imagen')  
    imagen = pygame.image.load(image)
    while True: 
        for eventos in pygame.event.get():
            if eventos.type == pygame.QUIT:
                sys.exit(0)
        ventana.blit(imagen,(0,0))
        pygame.display.update()
    return 0

pygame.init() 
main(argv[1])
