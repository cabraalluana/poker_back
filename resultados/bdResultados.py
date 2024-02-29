import sqlite3

# Conecta ao banco de dados (se não existir, ele será criado)
conn = sqlite3.connect('bdPoker.db')

# Define a codificação UTF-8 para o banco de dados
conn.execute('PRAGMA encoding = "UTF-8"')

# Cria um cursor para executar comandos SQL
cursor = conn.cursor()

# Cria a tabela TABELA_RESULTADOS
cursor.execute('''
               CREATE TABLE IF NOT EXISTS TABELA_RESULTADOS (
               idResultados INTEGER NOT NULL UNIQUE,
               idMesa INTEGER NOT NULL,
               primeiroLugar INTEGER NOT NULL,
               segundoLugar INTEGER NOT NULL,
               terceiroLugar INTEGER NOT NULL,
               PRIMARY KEY("idResultados" AUTOINCREMENT)
               FOREIGN KEY (idMesa) REFERENCES TABELA_MESA(idMesa)
               )
               ''')

def salvar_resultado(idMesa, primeiro_lugar, segundo_lugar, terceiro_lugar):
    # Insere os resultados na tabela
    cursor.execute('''
                   INSERT INTO TABELA_RESULTADOS (idMesa, primeiroLugar, segundoLugar, terceiroLugar)
                   VALUES (?, ?, ?, ?)
                   ''', (idMesa, primeiro_lugar, segundo_lugar, terceiro_lugar))
    
    # Commit das alterações e fechamento da conexão
    conn.commit()