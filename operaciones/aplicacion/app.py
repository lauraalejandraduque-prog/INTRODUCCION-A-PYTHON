from flask import Flask
from pulp import *
app = Flask(__name__)

@app.route("/")
def hello_world():

    modelo=LpProblem("ejemplo_inicial",LpMinimize)

    x1=LpVariable("Porcentaje de pollo",0)
    x2=LpVariable("Porcentaje de carne", 0)

    modelo+=0.013*x1 + 0.008*x2 #Función objetivo
    modelo+=x1+x2==100
    modelo += 0.100 * x1 + 0.200 * x2 >= 8.0, "ProteinRequirement"
    modelo += 0.080 * x1 + 0.100 * x2 >= 6.0, "FatRequirement"
    modelo += 0.001 * x1 + 0.005 * x2 <= 2.0, "FibreRequirement"
    modelo += 0.002 * x1 + 0.005 * x2 <= 0.4, "SaltRequirement"

    modelo.solve() #Instrucción para resolver el modelo
    #print(modelo)


    return f"el resultado de la función objetivo es: {value(modelo.objective)}, el valor de X1 es: {x1.varValue}, el valor de X2 es:{x2.varValue}"
