'''
Funciones:
son procedimientos personalizados podemos describir una actividad a ejecutar según algunos datos de entrada
tenemos 2 consideraciones:
    definición 
    uso
'''

#definición
#uso de palabra reservada def
#nombre
#parámetros
#return
def mi_funcion():
    #intrucciones
    return True

# uso
#llamamos a la función entregándole datos en los argumentos
print(mi_funcion())

import random 
def mi_aleatorio():
    return random.randint(1,100)
print(mi_aleatorio())


def mi_aleatorio_2(a,b):
    return random.randint(a,b)
print(mi_aleatorio_2(8,50))


x=90
y=100

def multiples_retornos():
    z=50
    return x,y,z

print(multiples_retornos())
#print(x,y,z) # las variables definidas dentro de la función solo viven en ella

#funciones con parámetros opcionales
def otra_funcion(a=True):
    return print("por defecto será True", "actualmente es", a)

#llamo a la función
otra_funcion(False)