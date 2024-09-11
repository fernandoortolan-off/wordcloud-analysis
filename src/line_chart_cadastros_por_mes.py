import main
import os

from pandas import DataFrame
import pandas as pd

import matplotlib.pyplot as plt


os.chdir('./')

diretorio = './csv/'
nome_do_arquivo_csv = main.nome_do_arquivo_csv

def gerar_listas_anos_cadastros(df : DataFrame, nome_coluna_data : str, nome_coluna_quant : int):
    """
    Gera duas listas: uma com todos os anos distintos e outra
    contendo listas que representam a quantidade de novos cadastros
    por mês, correspondendo à quantidade de anos da lista de anos
    distintos. Os dados são extraídos de um DataFrame.
    
    :param df: DataFrame contendo os dados.
    :param nome_coluna_data: Nome da coluna que contém as datas.
    :param nome_coluna_quant: Nome da coluna que contém as quantidades.
    """
    anos_distintos = []
    quant_por_mes = []

    for index, row in df.iterrows():
        data = str(row[nome_coluna_data])
        ano = data[0:4]
        if ano not in anos_distintos:
            anos_distintos.append(ano)
        anos_distintos.sort()
    
    for ano in anos_distintos:
        lista_ano = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for index, row in df.iterrows():
            data = str(row[nome_coluna_data])
            quant = int(row[nome_coluna_quant])
            ano_atual = data[0:4]
            mes = data[5:]
            if ano_atual == ano:
                lista_ano[int(mes) - 1] = quant
        quant_por_mes.append(lista_ano)
    
    return anos_distintos, quant_por_mes


def fazer_media_ate_ano_limite(anos_distintos : list, quant_por_mes : list, ano_limite : int):
    new_anos_distintos = anos_distintos.copy()
    new_quant_por_mes = quant_por_mes.copy()

    media = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    for i in range(0, len(new_anos_distintos)):
        ano = new_anos_distintos[0]
        if int(ano) <= ano_limite:
            for i in range(0, 12):
                media[i] = (media[i] + new_quant_por_mes[0][i])
            new_anos_distintos.pop(0)
            new_quant_por_mes.pop(0)
    new_anos_distintos.insert(0, f"Anterior a {ano_limite}")
    new_quant_por_mes.insert(0, media)

    return new_anos_distintos, new_quant_por_mes


df_cadastros_por_mes = pd.read_csv(f'{diretorio}{nome_do_arquivo_csv}', sep=';', encoding = 'utf-8')
lista_anos_distintos, lista_quant_por_mes = gerar_listas_anos_cadastros(df_cadastros_por_mes, 'ano_mes', 'quant')
lista_anos_distintos, lista_quant_por_mes = fazer_media_ate_ano_limite(lista_anos_distintos, lista_quant_por_mes, 2022)

print(lista_anos_distintos)
print(lista_quant_por_mes)
meses = ['Jan.', 'Fev.', 'Mar.', 'Abr.', 'Mai.', 'Jun.', 'Jul.', 'Ago.', 'Set.', 'Out.', 'Nov.', 'Dez.']

num_cores = len(lista_anos_distintos)
cmap = plt.get_cmap('viridis')
cores = [cmap(i / num_cores) for i in range(num_cores)]
for i in range(0, len(lista_anos_distintos)):
    plt.plot(meses, lista_quant_por_mes[i], color=cores[i], marker="o", linestyle="--")
plt.legend(lista_anos_distintos)
plt.xlabel("Meses")
plt.ylabel("Quant. de cadastros")
plt.title("Quantidade de novos cadastros por mês")
plt.show()
