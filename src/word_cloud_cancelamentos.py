import main
import gera_csv

import os
import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from collections import Counter
from pandas import DataFrame
from PIL import Image
from wordcloud import WordCloud, ImageColorGenerator, STOPWORDS


os.chdir('./')

id_cliente = main.id_cliente
diretorio_csv_resultados = gera_csv.diretorio
diretorio_wordclouds = f'./wordcloud_resultados/cancelamentos/{id_cliente}/'
os.makedirs(diretorio_wordclouds, exist_ok=True)  # Cria o diretório caso não exista

arquivos = [f for f in os.listdir(diretorio_csv_resultados) if os.path.isfile(os.path.join(diretorio_csv_resultados, f))]
# print(arquivos)

for arquivo in arquivos:
    ano = arquivo[len(arquivo) - 8:len(arquivo) - 4]

    nome_arquivo = f'cancelamentos_{ano}.png'
    caminho_arquivo = diretorio_wordclouds + nome_arquivo


    df_cancelamentos = pd.read_csv(f'{diretorio_csv_resultados}contagem_palavras_{ano}.csv', sep=',', encoding = 'utf-8')


    # Cria dicionário com os dados
    d = {}
    for palavra, contagem in df_cancelamentos.values:
        d[palavra] = contagem


    stopwords_ptbr = open('./txt/stopwords.txt').read()
    lista_stopwords = stopwords_ptbr.split('\n')

    # Remove palavras genéricas
    for stopword in lista_stopwords:
        d.pop(stopword, None)


    wordcloud = WordCloud(background_color='white',
                        width=1280,
                        height=720,
                        max_words=500,
                        )

    wordcloud.generate_from_frequencies(frequencies=d)
    plt.figure(figsize=(10, 10))  # Tamanho do gráfico
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.title(f'Cancelamentos {ano}')
    plt.axis('off')

    wordcloud.to_file(caminho_arquivo)

    # plt.show()
