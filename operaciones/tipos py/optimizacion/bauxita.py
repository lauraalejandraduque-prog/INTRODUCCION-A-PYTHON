# Aplicación web en Flask que resuelve el Problema de la Bauxita usando PuLP (programación lineal mixta)
# Autor:    Joan Sebastian Talaga Ospina

from flask import Flask, request, render_template # Flask para crear la aplicación web
from pulp import *          # PuLP para resolver el modelo de optimización

bauxita = Flask(__name__)         # Crear instancia de la app Flask

@bauxita.route("/")                # Ruta principal del sitio web

def modelo_bauxita():             # Función que ejecuta el modelo

    # Definición del modelo
  
    modelo = LpProblem("Problema_Bauxita", LpMinimize)

  
    # Conjuntos
  
    MINAS = ["A", "B", "C"]
    PLANTAS = ["B", "C", "D", "E"]
    ESMALTADO = ["D", "E"]

  
    # Parámetros
    
    # Costos y capacidades según el problema

    cap_mina = {"A": 36000, "B": 52000, "C": 28000}
    cap_planta = {"B": 40000, "C": 20000, "D": 30000, "E": 80000}
    cap_esmaltado = {"D": 4000, "E": 7000}

    costo_explotacion = {"A": 420, "B": 360, "C": 540} #Mina
    costo_fijo = {"B": 3000000, "C": 2500000, "D": 4800000, "E": 6000000} #Planta
    costo_produccion = {"B": 330, "C": 320, "D": 380, "E": 240} #Planta
    costo_esmaltado = {"D": 8500, "E": 5200} #Esmaltado

    # Costos de transporte de bauxita de la mina a la planta (i -> j)
    ctran_b = {
        ("A", "B"): 400, ("A", "C"): 2010, ("A", "D"): 510, ("A", "E"): 1920,
        ("B", "B"): 10, ("B", "C"): 630, ("B", "D"): 220, ("B", "E"): 1510,
        ("C", "B"): 1630, ("C", "C"): 10, ("C", "D"): 620, ("C", "E"): 940
    }

    # Costos de transporte de alúmina de la planta a esmaltado (j -> k)
    ctran_a = {
        ("B", "D"): 220, ("B", "E"): 1510,
        ("C", "D"): 620, ("C", "E"): 940,
        ("D", "D"): 0, ("D", "E"): 1615,
        ("E", "D"): 1465, ("E", "E"): 0
    }

    demanda = {"D": 1000, "E": 1200} # En P. Esmaltado
    rend_bauxita = {"A": 0.06, "B": 0.08, "C": 0.062} # rendimiento de la bauxita en las mina
    rend_alumina = 0.4 #Rendimiento de la lumina en las plantas

    # Variables de decisión

    # Toneladas de bauxita (X) de mina i a planta j
    x = LpVariable.dicts("x", (MINAS, PLANTAS), lowBound=0)

    # Toneladas de alúmina (Y) de planta j a esmaltado k
    y = LpVariable.dicts("y", (PLANTAS, ESMALTADO), lowBound=0)

    # 1 si la planta de alúmina j se abre
    w = LpVariable.dicts("w", PLANTAS, lowBound=0, upBound=1, cat=LpBinary)

   
    # Función objetivo: minimizar costo total anual
    
    modelo += (
        lpSum(costo_explotacion[i] * x[i][j] for i in MINAS for j in PLANTAS)
        + lpSum(costo_produccion[j] * y[j][k] for j in PLANTAS for k in ESMALTADO)
        + lpSum(costo_esmaltado[k] * y[j][k] for j in PLANTAS for k in ESMALTADO)
        + lpSum(ctran_b[(i, j)] * x[i][j] for i in MINAS for j in PLANTAS)
        + lpSum(ctran_a[(j, k)] * y[j][k] for j in PLANTAS for k in ESMALTADO)
        + lpSum(costo_fijo[j] * w[j] for j in PLANTAS)
    )

    
    # Restricciones
   
    # Capacidad de minas
    for i in MINAS:
        modelo += lpSum(x[i][j] for j in PLANTAS) <= cap_mina[i]

    # Capacidad de plantas de alúmina
    for j in PLANTAS:
        modelo += lpSum(x[i][j] for i in MINAS) <= cap_planta[j] * w[j]

    # Capacidad de esmaltado
    for k in ESMALTADO:
        modelo += lpSum(y[j][k] for j in PLANTAS) <= cap_esmaltado[k]

    # Demanda de aluminio terminado
    for k in ESMALTADO:
        modelo += lpSum(rend_alumina * y[j][k] for j in PLANTAS) == demanda[k]

    # Balance de masa (bauxita → alúmina)
    for j in PLANTAS:
        modelo += lpSum(rend_bauxita[i] * x[i][j] for i in MINAS) == lpSum(y[j][k] for k in ESMALTADO)

    
    # Solución
    
    modelo.solve()       # Resolver el modelo con el solver
    estado = LpStatus[modelo.status]    # Obtener estado de la solución (óptimo, infactible, etc.)
    costo = value(modelo.objective)    # Obtener valor de la función objetivo

    
    # Resultados básicos
    
    resultado = f"Estado: {estado}, Costo total: ${costo:,.2f}\n" #Estado y costo de la solución

    resultado += "\nPlantas abiertas:\n"    #Mostrar Las platas que se abren con el 1 y las que no con 0
    for j in PLANTAS:
        resultado += f"  {j}: {int(value(w[j]))}\n"

    resultado += "\nFlujos de bauxita (x_ij):\n"  #Mostrar las cantidades optimas a enviar de las minas a las plantas
    for i in MINAS:
        for j in PLANTAS:
            if value(x[i][j]) > 0:
                resultado += f"  {i}->{j}: {value(x[i][j]):.2f}\n"

    resultado += "\nFlujos de alúmina (y_jk):\n"    #Mostrar las cantidades optimas a enviar de las plantas a las de esmaltado
    for j in PLANTAS:
        for k in ESMALTADO:
            if value(y[j][k]) > 0:
                resultado += f"  {j}->{k}: {value(y[j][k]):.2f}\n"

   # return f"<pre>{resultado}</pre>"  #Mostrar el resultado 
    funcion_objetivo=value(modelo.objective)
    dato1=w['B'].varValue
    dato2=w['C'].varValue
    dato3=w['D'].varValue
    dato4=w['E'].varValue

    

    return render_template("bauxita.html", funcion_objetivo=funcion_objetivo,dato1=dato1,dato2=dato2,dato3=dato3,dato4=dato4)

if __name__ == "_main_":
    bauxita.run(debug=True)      # Ejecutar servidor