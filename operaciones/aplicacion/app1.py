from flask import Flask
from pulp import *
app = Flask(__name__)

@app.route("/")
def hello_world():
    modelo=LpProblem("La_bauxita", LpMinimize)
    
    #variables de decision
    #1) X_ij = Tonelada/año de bauxita a transportar desde la mina i hacia la planta de alúmina j; i = A, B, C; j = B, C, D, E. 
    X_ij = LpVariable.dicts("Tonelada_año_de_bauxita_a_transportar_desde_la_mina_i_hacia_la_planta_de_alúmina_j", 
                            (['A','B','C'], ['B','C','D','E']), lowBound=0)
    
    #2)Y_jk = Tonelada/año de alúmina a transportar desde la planta de alúmina j hacia la planta de esmaltado k; j = B, C, D, E; k = D, E. 
    Y_jk = LpVariable.dicts("Tonelada_año_de_alúmina_a_transportar_desde_la_planta_de_alúmina_j_hacia_la_planta_de_esmaltado_k", 
                            (['B','C','D','E'], ['D','E']), lowBound=0)
    #3)W_j =  1, si la planta de alúmina j se abre; 0, de lo contrario; j = B, C, D, E
    W_j = LpVariable.dicts("si_la_planta_de_alúmina_j_se_abre", 
                            (['B','C','D','E']), cat='Binary')
    
    #funcion objetivo
    #Costo anual de explotación de bauxita ($/año):
    Costo_anual_de_explotación_de_bauxita = ( 420*(X_ij['A']['B'] + X_ij['A']['C'] + X_ij['A']['D'] + X_ij['A']['E']) + \
                                              360*(X_ij['B']['B'] + X_ij['B']['C'] + X_ij['B']['D'] + X_ij['B']['E']) + \
                                              540*(X_ij['C']['B'] + X_ij['C']['C'] + X_ij['C']['D'] + X_ij['C']['E'])
                                            )
    
    #costo anual de producción de alúmina ($/año):
    Costo_anual_de_producción_de_alúmina = ( 330*(Y_jk['B']['D'] + Y_jk['B']['E']) + \
                                            320*(Y_jk['C']['D'] + Y_jk['C']['E']) + \
                                            380*(Y_jk['D']['D'] + Y_jk['D']['E']) + \
                                            240*(Y_jk['E']['D'] + Y_jk['E']['E'])
                                            )
    
    #Costo anual de procesamiento de alúmina en las plantas de esmaltado ($/año):
    Costo_anual_de_procesamiento_de_alúmina_en_las_plantas_de_esmaltado = ( 8500*(Y_jk['B']['D'] + Y_jk['C']['D'] + Y_jk['D']['D'] + Y_jk['E']['D']) + \
                                                                          5200*(Y_jk['B']['E'] + Y_jk['C']['E'] + Y_jk['D']['E'] + Y_jk['E']['E'])
                                                                        )
    
    #Costo anual de transporte desde las minas de bauxita hacia las plantas de alúmina ($/año):
    Costo_anual_de_transporte_de_bauxita_desde_las_minas_hacia_las_plantas_de_alúmina = ( 400*X_ij['A']['B'] + 2100*X_ij['A']['C'] + 510*X_ij['A']['D'] + 1920*X_ij['A']['E'] + \
                                                                                             10*X_ij['B']['B'] + 630*X_ij['B']['C'] + 220*X_ij['B']['D'] + 1510*X_ij['B']['E'] + \
                                                                                             1630*X_ij['C']['B'] + 10*X_ij['C']['C'] + 620*X_ij['C']['D'] + 940*X_ij['C']['E']
                                                                                                )

    #costo anual de transporte de alúmina desde las plantas de alúmina hacia las plantas de esmaltado ($/año):
    Costo_anual_de_transporte_de_alúmina_desde_las_plantas_de_alúmina_hacia_las_plantas_de_esmaltado = ( 220*Y_jk['B']['D'] + 620*Y_jk['C']['D'] + 1465*Y_jk['E']['D'] + \
                                                                                                 1510*Y_jk['B']['E'] + 940*Y_jk['C']['E'] + 1615*Y_jk['D']['E'] 
                                                                                                    )   
    
    #Costo fijo anual de las plantas de alúmina ($/año):
    Costo_fijo_anual_de_las_plantas_de_alúmina = ( 3000000*W_j['B'] + \
                                                  2500000*W_j['C'] + \
                                                    4800000*W_j['D'] + \
                                                    6000000*W_j['E']
                                                )
    

    modelo+= ( Costo_anual_de_explotación_de_bauxita 
    + Costo_anual_de_producción_de_alúmina 
    +Costo_anual_de_procesamiento_de_alúmina_en_las_plantas_de_esmaltado 
    + Costo_anual_de_transporte_de_bauxita_desde_las_minas_hacia_las_plantas_de_alúmina 
    + Costo_anual_de_transporte_de_alúmina_desde_las_plantas_de_alúmina_hacia_las_plantas_de_esmaltado 
    + Costo_fijo_anual_de_las_plantas_de_alúmina
    )

    #restricciones
    #1) Por capacidad anual de explotación de bauxita en cada mina (Tonelada de bauxita/año):
    modelo += X_ij['A']['B'] + X_ij['A']['C'] + X_ij['A']['D'] + X_ij['A']['E'] <= 36000, "capacidad_anual_de_explotación_de_bauxita_mina_A"
    modelo += X_ij['B']['B'] + X_ij['B']['C'] + X_ij['B']['D'] + X_ij['B']['E'] <= 52000, "capacidad_anual_de_explotación_de_bauxita_mina_B"
    modelo += X_ij['C']['B'] + X_ij['C']['C'] + X_ij['C']['D'] + X_ij['C']['E'] <= 28000, "capacidad_anual_de_explotación_de_bauxita_mina_C"

    #2) Por capacidad anual de procesamiento de bauxita en cada planta de alúmina (Tonelada de bauxita/año):
    modelo += X_ij['A']['B'] + X_ij['B']['B'] + X_ij['C']['B'] <= 40000*W_j['B'], "capacidad_anual_de_procesamiento_de_bauxita_planta_de_alúmina_B"
    modelo += X_ij['A']['C'] + X_ij['B']['C'] + X_ij['C']['C'] <= 20000*W_j['C'], "capacidad_anual_de_procesamiento_de_bauxita_planta_de_alúmina_C"
    modelo += X_ij['A']['D'] + X_ij['B']['D'] + X_ij['C']['D'] <= 30000*W_j['D'], "capacidad_anual_de_procesamiento_de_bauxita_planta_de_alúmina_D"
    modelo += X_ij['A']['E'] + X_ij['B']['E'] + X_ij['C']['E'] <= 80000*W_j['E'], "capacidad_anual_de_procesamiento_de_bauxita_planta_de_alúmina_E"

     # 3) Capacidad anual de procesamiento de alúmina en cada planta de esmaltado
    modelo += Y_jk['B']['D'] + Y_jk['C']['D'] + Y_jk['D']['D'] + Y_jk['E']['D'] <= 4000, "Capacidad_esmaltado_D"
    modelo += Y_jk['B']['E'] + Y_jk['C']['E'] + Y_jk['D']['E'] + Y_jk['E']['E'] <= 7000, "Capacidad_esmaltado_E"
    
    # 4) Ventas anuales de aluminio terminado en cada planta de esmaltado
    modelo += 0.4 * (Y_jk['B']['D'] + Y_jk['C']['D'] + Y_jk['D']['D'] + Y_jk['E']['D']) == 1000, "Demanda_planta_D"
    modelo += 0.4 * (Y_jk['B']['E'] + Y_jk['C']['E'] + Y_jk['D']['E'] + Y_jk['E']['E']) == 1200, "Demanda_planta_E"

    # 5) Balance de masa en cada planta de alúmina
    modelo += 0.060 * X_ij['A']['B'] + 0.080 * X_ij['B']['B'] + 0.062 * X_ij['C']['B'] == Y_jk['B']['D'] + Y_jk['B']['E'], "Balance_planta_B"
    modelo += 0.060 * X_ij['A']['C'] + 0.080 * X_ij['B']['C'] + 0.062 * X_ij['C']['C'] == Y_jk['C']['D'] + Y_jk['C']['E'], "Balance_planta_C"
    modelo += 0.060 * X_ij['A']['D'] + 0.080 * X_ij['B']['D'] + 0.062 * X_ij['C']['D'] == Y_jk['D']['D'] + Y_jk['D']['E'], "Balance_planta_D"
    modelo += 0.060 * X_ij['A']['E'] + 0.080 * X_ij['B']['E'] + 0.062 * X_ij['C']['E'] == Y_jk['E']['D'] + Y_jk['E']['E'], "Balance_planta_E"

     # Resolver el modelo
    # Resolver el modelo
    modelo.solve()

    estado = LpStatus[modelo.status]
    costo_total = value(modelo.objective)
    plantas_abiertas = {planta: value(W_j[planta]) for planta in ['B', 'C', 'D', 'E'] if value(W_j[planta]) > 0}
    cantidades_bauxita = {f'{mina}-{planta}': value(X_ij[mina][planta]) for mina in ['A', 'B', 'C'] for planta in ['B', 'C', 'D', 'E']}
    cantidades_alumina = {f'{planta}-{esmaltado}': value(Y_jk[planta][esmaltado]) for planta in ['B', 'C', 'D', 'E'] for esmaltado in ['D', 'E']}
    

    return f"El costo mínimo anual es: ${costo_total:,.2f}, Estado de la solución: {estado}, Plantas abiertas: {plantas_abiertas}, \n    Cantidades de Bauxita: {cantidades_bauxita}, \n    Cantidades de Alúmina: {cantidades_alumina}"

if __name__ == "__main__":
    app.run(debug=True)
