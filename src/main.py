# Configurar

# ID do cliente no IXC
id_cliente = 9480

# Nome do arquivo .csv que servirá de base para gerar as nuvens de palavras
# Query do .csv raiz em questão:
"""
SELECT obs_cancelamento, data_cancelamento FROM cliente_contrato WHERE `status` = 'I';
"""
# Salvar como CSV UTF-8 (Delimitado por Vírgulas) (.csv)
# Arquivo tem que estar presente na pasta "csv" na raiz do projeto
nome_do_arquivo_csv = 'obs_cancelamento.csv'
