import os
import re
# import numpy as np
import pandas as pd
# import matplotlib.pyplot as plt

from collections import Counter
from pandas import DataFrame
# from PIL import Image
# from wordcloud import WordCloud, ImageColorGenerator


def gerar_lista_anos_distintos(df : DataFrame, nome_coluna_tipo_date : str):
    """
    Gera uma lista ordenada de anos distintos extraídos de uma coluna de datas em um DataFrame.
    
    :param df: DataFrame contendo os dados.
    :param nome_coluna_tipo_date: Nome da coluna que contém as datas.
    """
    anos_distintos = []

    for index, row in df.iterrows():
        data = str(row[nome_coluna_tipo_date])
        ano = data[len(data) - 4:]  # Extrai o ano de uma data no formato dd/mm/yyyy, como '01/01/2010'
        if ano not in anos_distintos:
            anos_distintos.append(ano)

    anos_distintos.sort()

    # for ano in anos:
    #     print(ano)

    return anos_distintos


def gerar_csv_contagem_de_palavras(df : DataFrame, nome_coluna_obs : str, nome_arquivo_saida : str):
    """
    Gera uma lista ordenada de anos distintos extraídos de uma coluna de datas em um DataFrame.
    
    :param df: DataFrame contendo os dados.
    :param nome_coluna_obs: Nome da coluna que contém as observações dos cancelamentos.
    :param nome_arquivo_saida: Nome do arquivo .csv que será gerado no final da função
    """

    # Remove valores nulos da coluna 'nome_coluna_obs', une os textos
    # não nulos em uma única string, separando-os por espaço
    texto = ' '.join(df[f'{nome_coluna_obs}'].dropna())

    # Converte o texto para minúsculas e usa regex para encontrar
    # todas as palavras compostas por caracteres alfanuméricos
    palavras = re.findall(r'\b\w+\b', texto.lower())

    # Conta a frequência de cada palavra na lista 'palavras' e
    # armazena o resultado em um dicionário com a palavra como
    # chave e a contagem como valor
    contagem_palavras = Counter(palavras)
    
    # Converte a contagem em DataFrame
    contagem_palavras_df = pd.DataFrame(contagem_palavras.items(), columns=['palavra', 'contagem'])

    # Gera um csv
    contagem_palavras_df.to_csv(f'{nome_arquivo_saida}.csv', index=False)


def gerar_csv_por_ano(df : DataFrame, nome_coluna_tipo_date : str, lista_anos : list, nome_arquivo_saida : str):
    """
    Filtra o DataFrame por ano e gera arquivos CSV contendo a contagem de palavras para cada ano.
    
    :param df: DataFrame contendo os dados.
    :param nome_coluna_tipo_date: Nome da coluna que contém as datas.
    :param lista_anos: Lista de anos para filtrar.
    :param nome_arquivo_saida: Prefixo para o nome dos arquivos CSV de saída.
    """

    for ano in lista_anos:
        df_filtrado_por_ano = df[df[nome_coluna_tipo_date].str.contains(ano, na=False)]
        gerar_csv_contagem_de_palavras(df_filtrado_por_ano, 'obs_cancelamento', f'{nome_arquivo_saida}_{ano}')


os.chdir('./csv_testes')

# Query do .csv raiz: SELECT obs_cancelamento, data_cancelamento FROM cliente_contrato WHERE `status` = 'I';
# df_cancelamentos = pd.read_csv('obs_cancelamento.csv', sep=';', encoding = 'utf-8')
df_cancelamentos_light = pd.read_csv('obs_cancelamento2.csv', sep=';', encoding = 'utf-8')

lista_anos_distintos = gerar_lista_anos_distintos(df_cancelamentos_light, 'data_cancelamento')
gerar_csv_por_ano(df_cancelamentos_light, 'data_cancelamento', lista_anos_distintos, 'contagem_palavras')
