import main
import os

from pandas import DataFrame
import pandas as pd

import matplotlib.pyplot as plt


os.chdir('./')

id_cliente = main.id_cliente
nome_do_arquivo_csv = main.nome_do_arquivo_csv
diretorio_csv = './csv/'
diretorio_grafico_linha = f'./grafico_linha/novos_cadastros/{id_cliente}/'
os.makedirs(diretorio_grafico_linha, exist_ok=True)  # Cria o diretório caso não exista


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


def filtrar_listas_media_ate_ano_limite(anos_distintos : list, quant_por_mes : list, ano_limite : int):
    """
    Filtra as listas geradas pela função gerar_listas_anos_cadastros,
    calculando a média do número de cadastros em cada mês até o ano
    limite passado por parâmetro.
    
    Retorna as duas listas filtradas.
    
    :param anos_distintos: Lista de anos distintos gerada pela função gerar_listas_anos_cadastros.
    :param quant_por_mes: Lista de quantidades por mês gerada pela função gerar_listas_anos_cadastros.
    :param ano_limite: Ano limite para o cálculo da média.
    """
    new_anos_distintos = anos_distintos.copy()
    new_quant_por_mes = quant_por_mes.copy()

    media = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    pop_count = 0

    for i in range(0, len(new_anos_distintos)):
        ano = new_anos_distintos[0]
        if int(ano) <= (ano_limite - 1):
            for i in range(0, 12):
                media[i] = (media[i] + new_quant_por_mes[0][i])
            new_anos_distintos.pop(0)
            new_quant_por_mes.pop(0)
            pop_count += 1
    for i in range(0, 12):
        media[i] = (media[i] // pop_count)
    new_anos_distintos.insert(0, f"Anterior a {ano_limite}")
    new_quant_por_mes.insert(0, media)

    return new_anos_distintos, new_quant_por_mes


def verificar_maior_mes_de_crescimento_ate_ano_atual(anos_distintos : list, quant_por_mes):
    """
    Analisa as listas geradas pela função gerar_listas_anos_cadastros
    e retorna uma string conclusiva sobre o mês com o maior número de cadastros.
    
    :param anos_distintos: Lista de anos distintos gerada pela função gerar_listas_anos_cadastros.
    :param quant_por_mes: Lista de quantidades por mês gerada pela função gerar_listas_anos_cadastros.
    """
    media_ate_ano_limite = [0] * 12
    for i in range(0, (len(anos_distintos) - 1)):
        for j in range(0, 12):
            media_ate_ano_limite[j] = (media_ate_ano_limite[j] + quant_por_mes[i][j])
    
    meses = [
        'janeiro', 'fevereiro', 'março', 'abril',
        'maio', 'junho', 'julho', 'agosto',
        'setembro', 'outubro', 'novembro', 'dezembro'
    ]
    maior = media_ate_ano_limite[0]
    mes = 0
    for i in range(1, len(media_ate_ano_limite)):
        if media_ate_ano_limite[i] > maior:
            maior = media_ate_ano_limite[i]
            mes = i
    
    conclusao = f"O mês com o maior número de cadastros até 2024 é {meses[mes]}, com {maior} novos cadastros em todo o período."

    return conclusao


def gerar_grafico_de_linhas_n_cadastros_por_mes(dir_arquivos : str, nome_arquivo_csv : str, ano_limite : int, id_cliente : id, diretorio_final : str):
    """
    Gera um gráfico de linhas representando o número de cadastros em cada mês ao longo dos anos.
    
    :param dir_arquivos: String contendo o diretório onde está o arquivo .csv para gerar o DataFrame.
    :param nome_arquivo_csv: Nome do arquivo .csv que será analisado.
    :param ano_limite: Ano limite até o qual será feita a média.
    :param id_cliente: ID do cliente, utilizado para gerar o nome da imagem .png.
    :param diretorio_final: Diretório onde a imagem será salva.
    """

    df_cadastros_por_mes = pd.read_csv(f'{dir_arquivos}{nome_arquivo_csv}', sep=';', encoding = 'utf-8')

    lista_anos_distintos, lista_quant_por_mes = gerar_listas_anos_cadastros(df_cadastros_por_mes, 'ano_mes', 'quant')
    # print(lista_anos_distintos)
    # print(lista_quant_por_mes)

    conclusao = verificar_maior_mes_de_crescimento_ate_ano_atual(lista_anos_distintos, lista_quant_por_mes)

    lista_anos_distintos, lista_quant_por_mes = filtrar_listas_media_ate_ano_limite(lista_anos_distintos, lista_quant_por_mes, ano_limite)
    # print(lista_anos_distintos)
    # print(lista_quant_por_mes)

    meses = ['Jan.', 'Fev.', 'Mar.', 'Abr.', 'Mai.', 'Jun.', 'Jul.', 'Ago.', 'Set.', 'Out.', 'Nov.', 'Dez.']

    num_cores = len(lista_anos_distintos)
    cmap = plt.get_cmap('viridis')
    cores = [cmap(i / num_cores) for i in range(num_cores)]

    plt.figure(figsize=(20, 7.5))

    for i in range(0, len(lista_anos_distintos)):
        plt.plot(meses, lista_quant_por_mes[i], color=cores[i], marker="o", linestyle="--")
    
    plt.title("Quantidade de novos cadastros por mês")
    plt.legend(lista_anos_distintos)
    plt.xlabel("Meses")
    plt.ylabel("Quant. de cadastros")
    plt.text(0, 0, f"Conclusão: {conclusao}", fontsize=11, color='green')

    plt.savefig(f'{diretorio_final}cadastros_por_mes_{id_cliente}.png')
    
    # plt.show()


gerar_grafico_de_linhas_n_cadastros_por_mes(diretorio_csv, nome_do_arquivo_csv, 2022, id_cliente, diretorio_grafico_linha)
