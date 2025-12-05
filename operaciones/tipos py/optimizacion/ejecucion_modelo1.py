from modelo import optimizar
import random

print(optimizar(0.013,0.008))
print(optimizar(0.010,0.010))

for i in range(1,10):
    costo1=random.random()
    costo2=random.random()
    print(optimizar(costo1, costo2))

    