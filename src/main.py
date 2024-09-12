# Configurar

# ID do cliente no IXC
id_cliente = 7461


# Query do .csv raiz da nuvem de palavras das observações de cancelamentos:
"""
SELECT obs_cancelamento, data_cancelamento FROM cliente_contrato WHERE `status` = 'I';
"""
# nome_do_arquivo_csv = 'obs_cancelamento_light_9480.csv'


# Query do .csv raiz do gráfico de linhas das quantidades de cadastros por mês/ano:
"""
SELECT LEFT(data_cadastro, 7) AS 'ano_mes', count(*) AS 'quant' FROM cliente WHERE data_cadastro IS NOT NULL AND data_cadastro <> '0000-00-00' GROUP BY LEFT(data_cadastro, 7);
"""
nome_do_arquivo_csv = 'cadastros_por_mes_7461.csv'


# Salvar como CSV UTF-8 (Delimitado por Vírgulas) (.csv)
# Arquivo tem que estar presente na pasta "csv" na raiz do projeto
