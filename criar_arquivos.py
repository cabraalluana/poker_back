import sqlite3
import os
import shutil

try:
    # Conexão com o banco de dados
    conn = sqlite3.connect('bdPoker.db')
    cursor = conn.cursor()

    # Consulta para obter os nomes dos arquivos da tabela
    cursor.execute("SELECT arquivo FROM TABELA_CODIGO")
    arquivos = cursor.fetchall()

    # Pasta onde os arquivos serão criados
    pasta_destino = 'arquivos'

    # Verificando se a pasta de destino existe, se não, criando-a
    if not os.path.exists(pasta_destino):
        os.makedirs(pasta_destino)
    else:
        # Itera sobre todos os arquivos na pasta
        for arquivo in os.listdir(pasta_destino):
            try:
                # Monta o caminho completo do arquivo
                caminho_arquivo = os.path.join(pasta_destino, arquivo)
                # Verifica se é um arquivo e não um diretório
                if os.path.isfile(caminho_arquivo):
                    # Remove o arquivo
                    os.unlink(caminho_arquivo)
                # Se for um diretório, remove recursivamente
                elif os.path.isdir(caminho_arquivo):
                    shutil.rmtree(caminho_arquivo)
            except Exception as e:
                print(f"Erro ao apagar {caminho_arquivo}: {e}")

    # Loop sobre os nomes dos arquivos e criação dos arquivos
    for arquivo in arquivos:
        nome_arquivo = arquivo[0]  # O nome do arquivo está na primeira coluna
        caminho_arquivo = os.path.join(pasta_destino, nome_arquivo)
        
        # Verifica se o arquivo já existe
        if not os.path.exists(caminho_arquivo):
            # Criação do arquivo vazio apenas se ele não existir
            with open(caminho_arquivo, 'w') as f:
                pass  # Não é necessário escrever nada, arquivo será vazio

    # Fechando a conexão com o banco de dados
    conn.close()

except sqlite3.Error as e:
    print("Erro ao acessar o banco de dados:", e)

except IOError as e:
    print("Erro de I/O ao criar o arquivo:", e)
