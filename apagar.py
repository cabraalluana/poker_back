import sqlite3

# Conectando ao banco de dados (se não existir, ele será criado)
conn = sqlite3.connect('bdPoker.db')

# Criando um cursor para executar operações SQL
cursor = conn.cursor()

# Comando SQL para apagar a tabela
sql_query = "DROP TABLE IF EXISTS TABELA_RESULTADOS;"

# Executando o comando SQL
cursor.execute(sql_query)

# Commit das alterações (necessário para salvar as alterações)
conn.commit()

# Fechando a conexão com o banco de dados
conn.close()
