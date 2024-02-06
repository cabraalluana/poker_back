import sqlite3
import os

# Conexão com o banco de dados
conn = sqlite3.connect('bdPoker.db')
cursor = conn.cursor()

# Consulta para obter os nomes dos arquivos da tabela
cursor.execute("SELECT arquivo FROM TABELA_CODIGO")
arquivos = cursor.fetchall()

# Pasta onde os arquivos serão criados
pasta_destino = 'arquivos'

# Loop sobre os nomes dos arquivos e criação dos arquivos
for arquivo in arquivos:
    nome_arquivo = arquivo[0]  # O nome do arquivo está na primeira coluna
    caminho_arquivo = os.path.join(pasta_destino, nome_arquivo)
    
    # Criação do arquivo vazio
    with open(caminho_arquivo, 'w') as f:
        f.write('')  # Cria um arquivo vazio

# Fechando a conexão com o banco de dados
conn.close()
