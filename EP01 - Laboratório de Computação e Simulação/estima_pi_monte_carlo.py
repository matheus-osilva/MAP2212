import random
import math
def estimaPi(Seed = None):
    random.seed(Seed)
    n = 10000
    z = 2.57
    while True:
        pontos_no_circulo = 0
        pontos_totais = 0
        #gera os pontos e armazena os que caíram dentro do círculo
        for i in range(n):
            x = random.random()
            y = random.random()
            ponto = math.sqrt(x**2+y**2)
            if ponto <= 1: pontos_no_circulo += 1
            pontos_totais += 1
        pi_estimado = pontos_no_circulo/pontos_totais #estima pi/4
        var = abs((pi_estimado + (1 - pi_estimado)))
        erro = z * math.sqrt(var)/math.sqrt(pontos_totais)
        if erro <= 0.0005 * pi_estimado: break
        else:
            n = int(((z**2 * var)/(0.0005 * pi_estimado) ** 2) * 1.1)
    return (4 * pi_estimado, n)

output = estimaPi()
print("pi estimado:", output[0])
print("n: ", output[1])