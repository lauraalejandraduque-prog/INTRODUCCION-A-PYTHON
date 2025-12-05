'''
TIPOS DE DATOS
String : cadenas de texto ""  o ''
int
float
boolean

ESTRUCTURAS DE DATOS
sets : {} instanciamos con new Set
    nos sirven para almacenar datos únicos
    type class: 'set'>
    no interesa el orden de los elemnetos

listas : [] instanciamos con new List
tuplas: () instanciamos con tuple 
diccionarios {clave1:valor1, clave2:valor2, claveN:valorN} instanciamos con Dict
'''


conjunto={1,2,3,5,6,9,2}
print(conjunto)
print(type(conjunto))
conjunto2={5,10,'2',3,6,9,}
print(conjunto2)

#Metodos "Qué podemos hacer con los objetos"
conjunto.add(8)
print(conjunto) #{1,2,3,5,6,'2',8,9}
conjunto.pop()
print(conjunto) #{2,3,5,6,8,9,'2'}
print(conjunto.intersection(conjunto2))
print("metodo union",conjunto.union(conjunto2)) #{5,10,"2",3,6,9} metodo union {2,3,5,6,8,9}

#tuplas
tupla1=(4,5,"9",5)
tupla2=(3,9,"uv")

#print(type(tupla1))
#print(tupla1)
#print(tupla1.count("b"))
#print(tupla1.index("5")) #posicion de un elemento en el objeto

#listas
lista1=[True, "true", 5, "b", 10, 10]
print(type(lista1))
lista1.clear()
print(lista1)

''''
index:
clear: 
remove: elimina el elemento indicado una sola vez 
pop: elimina y retorna el elemento ubicado en la posicion indicada
'''

#diccionarios 
usuario1={"nombre":"Laura", "email":"laura@univalle", "password":1234, "estudiante": True}
print(type(usuario1))
print(usuario1.keys())
print(usuario1.values())
usuario1.clear()
print(usuario1)

#acceder a informacion
lista_=[5, 3, 9, 10]
print(lista_[0])
print(lista_[-1])
print(lista_[-2])
print(lista_[2:])
print(lista_[:])
print(lista_[2:4])
print(lista_[-4:-1])

tupla20=(2,9,5,6,3,"uv")
print(tupla20[2])


#acceder a un diccionario
curso={"nombre":"TDMI", "cantidad":20, "cancelar":"si"}
print(curso["cantidad"])
curso["cancelar"]="no"
print(curso)


#ejercicios 
#2.20
usuario2={"Liliana":4.5, "Carmen":3.3, "Josefina":4.1, "Daniela": 4.9, "Pedro":2.9, "José":4.6, "Mario":3.3}
print(type(usuario2))
print(usuario2.keys())
print(usuario2.values())

#2.22
#usuario2.popitem({'Daniela':4.9}) 
###nos está diciendo que se está utilizando mal el método, este funciona sin parámetros y se le pasó uno
##este método es util cuando se quiere eliminar el último elemento insertado en el diccionario sin importar la clave


#2.24 Sobre el diccionario calificaciones 
#aplique el método update verificando los argumentos necesarios para el  correcto funcionamiento si se quiere  modificar la nota asignada a la  estudiante Liliana a un valor de 4.7. 

usuario2.update({"Liliana": 4.7})
print(usuario2)

# 2.21 
usuario2= {"Liliana":4.5, "Carmen":3.3, "Josefina":4.1, "Daniela":4.9, "Pedro":2.9, "José":4.6, "Mario":3.3 }
print(sorted(usuario2)) #ordena alfabeticamente las claveres del diccionario, es decir, toma solo los nombres de los estudiantes y los ordena alfabeticamente

#En terminos de necesidad la funcion sorted() no es tan necesaria, ya que la informacion 
#necesaria ya se muestra en el diccionario, pero en terminos de orden si lo es, 
#ya que facilita la busqueda de un nombre en especifico

#2.23
print(usuario2.items()) #esta funcion devuelve una lista de que parece una lista de tuplas, es decir clave-valor, retorna un objeto tipo dict_items