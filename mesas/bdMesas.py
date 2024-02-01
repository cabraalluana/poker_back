# Importa a biblioteca SQLite
import sqlite3

# Conectar ao banco de dados
conn = sqlite3.connect('bdPoker.db')

# Define a codificação UTF-8 para o banco de dados
conn.execute('PRAGMA encoding = "UTF-8"')

# Cria um cursor para executar comandos SQL
cursor = conn.cursor()

# Cria a tabela TABELA_MESA se não existir
cursor.execute("""
               CREATE TABLE IF NOT EXISTS "TABELA_MESA" (
	           "idMesa"    INTEGER NOT NULL UNIQUE,
               "status"    TEXT NOT NULL,
               PRIMARY KEY("idMesa" AUTOINCREMENT)
               );
               """)

# Cria a tabela CODIGO_MESA se não existir
cursor.execute("""
               CREATE TABLE IF NOT EXISTS "CODIGO_MESA" (
               "idCodigoMesa"    INTEGER NOT NULL UNIQUE,
               "idCodigo"    INTEGER NOT NULL,
               "idMesa"    INTEGER NOT NULL,
               PRIMARY KEY("idCodigoMesa" AUTOINCREMENT),
               FOREIGN KEY("idCodigo") REFERENCES "TABELA_CODIGO"("idCodigo"),
               FOREIGN KEY("idMesa") REFERENCES "TABELA_MESA"("idMesa")
               );
               """)

def criar_mesa_e_vincular_codigos(listas_de_codigos):
    try:
        # Inicia uma transação
        conn.execute("BEGIN TRANSACTION")
        
        # Itera sobre as listas de códigos
        for i, lista_de_codigos in enumerate(listas_de_codigos, start=1):
            # Insere uma nova mesa com status "ativo"
            cursor.execute("INSERT INTO TABELA_MESA (status) VALUES (?)", ('ativo',))
            mesa_id = cursor.lastrowid  # Obtém o ID da última mesa inserida
            
            # Vincula os códigos à mesa na tabela CODIGO_MESA
            for codigo_id in lista_de_codigos:
                cursor.execute("INSERT INTO CODIGO_MESA (idMesa, idCodigo) VALUES (?, ?)", (mesa_id, codigo_id))
        
        # Comita as alterações no banco de dados
        conn.execute("COMMIT")
        print("Mesas e códigos vinculados com sucesso.")
        
    except Exception as e:
        # Em caso de erro, desfaz as alterações
        conn.execute("ROLLBACK")
        print(f"Erro ao criar mesas e vincular códigos: {e}")

def obter_id_mesas():
    query = "SELECT idMesa FROM TABELA_MESA"

    # Execute a consulta
    cursor.execute(query)

    # Obtenha os resultados usando fetchall()
    return cursor.fetchall()
    

def consultar_mesas_e_codigos(id_mesas):
    resultados = []
    
    # Consultar os dados desejados para cada ID de mesa fornecido
    for id_mesa in id_mesas:
        # Executar a consulta SQL parametrizada
        cursor.execute("""
            SELECT TABELA_MESA.idMesa, CODIGO_MESA.idCodigo, TABELA_USUARIO.nome
            FROM TABELA_MESA
            INNER JOIN CODIGO_MESA ON TABELA_MESA.idMesa = CODIGO_MESA.idMesa
            INNER JOIN TABELA_CODIGO ON CODIGO_MESA.idCodigo = TABELA_CODIGO.idCodigo
            INNER JOIN TABELA_USUARIO ON TABELA_CODIGO.idUsuario = TABELA_USUARIO.idUsuario
            WHERE TABELA_MESA.idMesa = ?
        """, (id_mesa,))

        # Adicionar os resultados da consulta à lista de resultados
        resultados.append(cursor.fetchall())

    return resultados