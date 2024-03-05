# Importa a biblioteca SQLite
import sqlite3

# Conectar ao banco de dados
conn = sqlite3.connect('bdPoker.db')

# Define a codificação UTF-8 para o banco de dados
conn.execute('PRAGMA encoding = "UTF-8"')

# Cria um cursor para executar comandos SQL
cursor = conn.cursor()

cursor.execute("""
        SELECT COUNT(*)
        FROM TABELA_CODIGO
        WHERE idCodigo NOT IN (
            SELECT idCodigo
            FROM CODIGO_MESA
            INNER JOIN TABELA_MESA ON CODIGO_MESA.idMesa = TABELA_MESA.idMesa
            WHERE TABELA_MESA.status = '1'
        )
    """)

print(cursor.fetchone()[0])