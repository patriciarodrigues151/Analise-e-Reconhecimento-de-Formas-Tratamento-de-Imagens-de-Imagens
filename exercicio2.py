# -*- coding: utf-8 -*-
"""Exercicio2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1iMwa1Dzjpijy88w7zDAHjyNHX634TS-1
"""

import numpy as np
import matplotlib.pyplot as plt
from skimage import data

"""Para calcular a subamostragem por média com o objetivo de reduzir a resolução da imagem por meio da amostragem , devemos:
Após determinar as dimensões da imagem, podemos remover as ultimas linhas e colunas da imagem que não podem ser divididas de maneira uniforme pelo fator de subamostragem. Após isso, podemos dividir a imagem de modo que ela fique dividida em blocos de 2x2 pixels.
"""

# Função para realizar subamostragem 2D por média
def subamostrar_2D(imagem, fator):
    linhas, colunas = imagem.shape
    imagem_ajustada = imagem[:linhas - linhas % fator, :colunas - colunas % fator]
    imagem_subamostrada = imagem_ajustada.reshape(linhas // fator, fator, colunas // fator, fator).mean(axis=(1, 3))
    return imagem_subamostrada

"""Os niveis são calculados usando potências de 2. Para normalizar a imagem, dividimos todos os valores dos pixels por 255 (valor maximo possivel pata pixels de 8 bits). Para fazer a quantização, a normalizada é multiplicada pelo numero de niveis de quantização, e depois arredondada o valor maximo. (nesse passo é feita a quantização e depois o processo inverso)"""

# Função para simular a quantização para imagens
def quantizar_imagem(imagem, bits):
    niveis = 2 ** bits
    imagem_quantizada = np.round(imagem / 255 * (niveis - 1)) / (niveis - 1) * 255
    return imagem_quantizada.astype(np.uint8)

"""a função np.linspace calcula os valores da função senoidal para cada valor do array t"""

# Função para gerar o sinal 1D
def geraSinal(N, w):
    t = np.linspace(0, 2*np.pi, N)
    sinal = np.sin(w * t)
    return sinal

"""recebe o sinal e o fator de subamostragem e faz o reshape"""

# Função para realizar amostragem por média
def amostragem(sinal, fator):
    return np.mean(sinal.reshape(-1, fator), axis=1)

"""da mesma forma, aqui os valores usam niveis de potencia de 2. Para normalizar a imagem entre -1 e 1, é adicionado 1 e dividido por 2 aos valores do sinal. Para quantizar, os valores normalizados são muiltiplicados pela quantidade de níveis e arredondados para os valores mais próximos. Após isso, a normalização é revertida fazendo o processo inverso, algo que os traz de volta a faixa original dos valores do sinal"""

# Função para simular a quantização
def quantizacao(sinal, bits):
    niveis = 2 ** bits
    sinal_quantizado = np.round((sinal + 1) * (niveis - 1) / 2) / (niveis - 1) * 2 - 1
    return sinal_quantizado

"""Teste para o caso 1D"""

# Caso 1D
N = 1000
w = 1.0

sinal_original = geraSinal(N, w)

resolucoes = [N, N // 2, N // 4, N // 8]
bits_quantizacao = [10, 5, 3, 1]

plt.figure(figsize=(12, 8))

for res in resolucoes:
    sinal_subamostrado = amostragem(sinal_original, N // res)
    plt.subplot(2, 2, resolucoes.index(res) + 1)
    plt.plot(sinal_original, label='Original')
    plt.plot(sinal_subamostrado, label=f'Subamostrado ({res})')
    plt.legend()

plt.tight_layout()
plt.show()

"""Teste para o caso 2D"""

# Caso 2D
imagem = data.camera()

resolucoes_2D = [imagem.shape[0], imagem.shape[0] // 2, imagem.shape[0] // 4, imagem.shape[0] // 8]

plt.figure(figsize=(12, 8))

for res in resolucoes_2D:
    imagem_subamostrada = subamostrar_2D(imagem, imagem.shape[0] // res)
    imagem_quantizada = quantizar_imagem(imagem_subamostrada, bits_quantizacao[0])
    plt.subplot(2, 2, resolucoes_2D.index(res) + 1)
    plt.imshow(imagem_quantizada, cmap='gray')
    plt.title(f'Resolução: {res}')

plt.tight_layout()
plt.show()