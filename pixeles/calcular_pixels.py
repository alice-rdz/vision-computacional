from sys import argv
from math import floor,sqrt

def calcular_pixeles(pixeles,cadena):
    cadena.lower()
    letra=cadena[0]
    serie = 'pkmt'
    for i in serie:
        if (i == letra):
            break
        else:
            pixeles *= 1024
            
    return pixeles
        
def calcular_dimension(pixeles,dimension):
    dimension = dimension.split(":")
    a=int(dimension[0])
    b=int(dimension[1])
    return a,b

def calcular():
    num = int(argv[1])
    cadena = argv[2]
    dimension = argv[3]
    pixeles=calcular_pixeles(num,cadena)
    a,b=calcular_dimension(pixeles,dimension)
    x =floor(sqrt(pixeles/(a*b)))
    print x
    dimensionx = a*x
    dimensiony = b*x
    return pixeles,dimensionx,dimensiony

def main():
    pixeles,x,y = calcular()
    print 'Pixeles:',pixeles
    print 'Dimensiones x=%d y=%d'%(x,y)

main()
