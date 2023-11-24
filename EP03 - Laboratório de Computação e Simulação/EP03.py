import random
import time
from math import cos, exp, log, sqrt
from scipy.stats import qmc

INFO = {13696262: "Matheus Oliveira da Silva"}
A = 0.592216676  # A = 0.rg
B = 0.49752833870  # B = 0.cpf


def f(x):
    # Função principal que estimaremos a integração
    return exp((-A) * x) * cos(B * x)


def simula_exponencial(u):
    # Funçao que auxilia para a simulação de uma distribuição exponencial, truncada entre [0, 1], para lambda igual a 0,5
    c = 2.5415  # Constante para truncar a exponencial
    lam = 0.5  # Lambda utilizado
    return log(1 - (u / c)) / (-lam)


def g(x):
    # Função que auxilia no método Importance Sapling
    c = 2.5415  # Constante para truncar a exponencial
    lam = 0.5  # Lambda utilizado
    return (c) * (lam * exp(-lam * x))


def h(x):
    # Função que auxilia no método Control Variates
    return 1 - A * x


def crude(Seed=None):
    random.seed(Seed)
    n = 10699142  # Define o tamanho da amostra

    # Inicia uma lista vazia que irá receber os valores de y
    lista_valores = []
    for i in range(n):
        # Gera um número aleatório entre 0 e 1 e calcula o
        # valor da função para esse número
        #y = f(random.random())
        generator = qmc.Halton(1)
        sample = generator.random(1)
        y = f(sample[0][0])
        # Adiciona o y a lista de valores
        lista_valores.append(y)
    y_estimado = sum(lista_valores) / n
    # Calcula o tamanho da amostra - alterar o n para o n piloto de 1000
    '''
    soma = 0
    for val in lista_valores:
        soma += (val - y_estimado) ** 2
    var = soma / (n - 1)
    n = (16 * (var) * (1.96 ** 2)) / (((y_estimado) * 0.0005) ** 2)
    print("media crude: ", y_estimado)
    print("variancia crude: ", var)
    print("N crude sera: ", n)
    print()
    '''
    return y_estimado # Retorna a média dos valores calculados


def hit_or_miss(Seed=None):
    random.seed(Seed)
    n = 86470557  # Define o tamanho da amostra

    # Inicia uma lista vazia que irá receber os valores (0 ou 1)
    lista_valores = []
    for i in range(n):
        # Gera dois numeros aleatórios entre 0 e 1 e verifica se
        # eles pertencem, ou não, a área abaixo da curva, devolvendo um valor 0 (não) ou 1 (sim)
        generator = qmc.Halton(2)
        sample = generator.random(1)
        indicador = sample[0][0] <= f(sample[0][1])
        # Adiciona o indicador a lista de valores
        lista_valores.append(indicador)
    y_estimado = sum(lista_valores) / n
    # Calcula o tamanho da amostra - alterar o n para o n piloto de 1000
    '''
    soma = 0
    for val in lista_valores:
        soma += (val - y_estimado) ** 2
    var = soma / (n - 1)
    n = (16 * (var) * (1.96 ** 2)) / (((y_estimado) * 0.0005) ** 2)
    print("media hit or miss: ", y_estimado)
    print("variancia hit or miss: ", var)
    print("N hit or miss sera: ", n)
    print()
    '''
    return y_estimado  # Retorna a estimativa, como sendo a proporção de ponto que pertencem a área abaixo da curva


def control_variate(Seed=None):
    start = time.time()
    random.seed(Seed)
    area_hx = 0.703891662  # Integral de h(x) no intervalo [0, 1], definido como omega no relatório
    n = 248163  # Define o tamanho da amostra

    # Inicia uma lista vazia que irá receber os valores de y
    lista_valores = []
    for i in range(n):
        # x = random.random()
        generator = qmc.Halton(1)
        sample = generator.random(1)
        x = f(sample[0][0])
        y = f(x) - h(x) + area_hx
        # Adiciona o indicador a lista de valores
        lista_valores.append(y)
    y_estimado = sum(lista_valores) / n
    # Calcula o tamanho da amostra - alterar o n para o n piloto de 1000
    '''
    soma = 0
    for val in lista_valores:
        soma += (val - y_estimado) ** 2
    var = soma / (n - 1)
    n = (16 * (var) * (1.96 ** 2)) / (((y_estimado) * 0.0005) ** 2)
    print("media control variate: ", y_estimado)
    print("variancia control variate: ", var)
    print("N control variate sera: ", n)
    print()
    '''
    end = time.time()
    print("Tempo control variate: ", end - start)
    return y_estimado  # Retorna a estimativa, como sendo a proporção de ponto que pertencem a área abaixo da curva


def importance_sampling(Seed=None):
    start = time.time()
    random.seed(Seed)
    n = 948576  # Define o tamanho da amostra

    # Inicia uma lista vazia que irá receber os valores de y
    lista_valores = []
    for i in range(n):
        # u = random.random()
        generator = qmc.Halton(1)
        sample = generator.random(1)
        u = f(sample[0][0])
        x = simula_exponencial(u)
        y = f(x) / g(x)
        lista_valores.append(y)
    y_estimado = sum(lista_valores) / n
    # Calcula o tamanho da amostra - alterar o n para o n piloto de 1000
    '''
    soma = 0
    for val in lista_valores:
        soma += (val - y_estimado) ** 2
    var = soma / (n - 1)
    n = (16 * (var) * (1.96 ** 2)) / (((y_estimado) * 0.0005) ** 2)
    print("media importance sampling: ", y_estimado)
    print("variancia importance sampling: ", var)
    print("N importance sampling sera: ", n)
    print()
    '''
    end = time.time()
    print("o tempo do importance foi de: ", end - start)
    return y_estimado  # Retorne sua estimativa


def main():
    while (True):
        inp = input("Insira 1 para Crude; 2 para Hit or Miss; 3 para Control Variate; 4 para Importance Sampling")
        match inp:
            case "1":
                print("crude: ", crude())
            case "2":
                print("hit or miss: ", hit_or_miss())
            case "3":
                print("control variate: ", control_variate())
            case "4":
                print("importance sampling: ", importance_sampling())
main()