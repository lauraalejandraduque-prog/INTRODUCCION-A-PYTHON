from pulp import *

def  optimizar (costo1, costo2):
    modelo=LpProblem("ejemplo_inicial",LpMinimize)

    x1=LpVariable("Porcentaje de pollo",0)
    x2=LpVariable("Porcentaje de carne", 0)

    modelo+=costo1*x1 + costo2*x2 #Función objetivo
    modelo+=x1+x2==100
    modelo += 0.100 * x1 + 0.200 * x2 >= 8.0, "ProteinRequirement"
    modelo += 0.080 * x1 + 0.100 * x2 >= 6.0, "FatRequirement"
    modelo += 0.001 * x1 + 0.005 * x2 <= 2.0, "FibreRequirement"
    modelo += 0.002 * x1 + 0.005 * x2 <= 0.4, "SaltRequirement"

    modelo.solve() #Instrucción para resolver el modelo
    #print(modelo)


    return LpStatus[modelo.status], value(modelo.objective)
