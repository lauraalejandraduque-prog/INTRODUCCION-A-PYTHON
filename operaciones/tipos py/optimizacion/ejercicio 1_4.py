'''
escriba un programa que capture del usuario dos valores a y b en dos inputs sucesivos.
Pida al usuario desde la función input que los valores a 
ingresar deben contener al menos un número 
decimal.  Al ejecutar, el programa debe realizar la 
multiplicación entre los dos valores y entregar la 
respuesta en un formatted string que contenga 
una variable llamada resultado y el texto de su 
preferencia. 
'''

entrada1=int(input("ingrese el primer valor: "))
entrada2=float(input("ingrese el segundo valor: "))

b=entrada1*entrada2

print("el resultado de la multiplicación es: ",b)
