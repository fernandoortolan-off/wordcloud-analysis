import main

import os
import re
import pandas as pd

from collections import Counter
from pandas import DataFrame


os.chdir('./')

id_cliente = main.id_cliente
nome_do_arquivo_csv = main.nome_do_arquivo_csv

diretorio = f'./csv_resultados/cancelamentos/{id_cliente}/'
os.makedirs(diretorio, exist_ok=True)  # Cria o diretório caso não exista


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

    for ano in anos_distintos:
        if ano.isnumeric() is False:
            anos_distintos.remove(ano)

    return anos_distintos


def gerar_csv_contagem_de_palavras(df : DataFrame, nome_coluna_obs : str, nome_arquivo_saida : str):
    """
    Gera uma lista ordenada de anos distintos extraídos de uma coluna de datas de um DataFrame.
    
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
    contagem_palavras_df.to_csv(f'{diretorio}{nome_arquivo_saida}.csv', index=False)


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


# Lê o .csv como um DataFrame
df_cancelamentos = pd.read_csv(f'csv/{nome_do_arquivo_csv}', sep=';', encoding = 'utf-8')

# Gera uma lista ordenada de anos distintos extraídos do DataFrame declarado anteriormente
lista_anos_distintos = gerar_lista_anos_distintos(df_cancelamentos, 'data_cancelamento')

gerar_csv_por_ano(df_cancelamentos, 'data_cancelamento', lista_anos_distintos, 'contagem_palavras')
