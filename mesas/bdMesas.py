# Importa a biblioteca SQLite
import sqlite3
import os

# Conectar ao banco de dados
conn = sqlite3.connect('bdPoker.db')

# Define a codificação UTF-8 para o banco de dados
conn.execute('PRAGMA encoding = "UTF-8"')

# Cria um cursor para executar comandos SQL
cursor = conn.cursor()

# Cria a tabela TABELA_MESA se não existir
cursor.execute('''
    CREATE TABLE IF NOT EXISTS TABELA_MESA (
        idMesa INTEGER PRIMARY KEY AUTOINCREMENT,
        status INTEGER NOT NULL DEFAULT 0 CHECK (status IN (0, 1))
    )
''') #0 - representa mesas inativas e 1 - representa mesas ativas

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
            cursor.execute("INSERT INTO TABELA_MESA (status) VALUES (?)", ('1',))
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

def obter_id_mesas(status):
    # Consulta SQL para obter os ids de mesas com o status fornecido
    query = "SELECT idMesa FROM TABELA_MESA WHERE status = ?"

    # Executar a consulta
    cursor.execute(query, (status,))
    id_mesas = [row[0] for row in cursor.fetchall()]

    return id_mesas
    

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

        # Verificar se há resultados na consulta
        rows = cursor.fetchall()
        if not rows:  # Se não houver resultados, adicione a mensagem de "Dado apagado do sistema"
            resultados.append("Dado apagado do sistema")
        else:  # Caso contrário, adicione os resultados à lista de resultados
            resultados.append(rows)

    return resultados

def criar_pastas_mesas_ativas(caminho_pasta):
    # Consulta para selecionar idMesa em que status = 1 (mesa ativa)
    cursor.execute("SELECT idMesa FROM TABELA_MESA WHERE status = 1")
    
    return cursor.fetchall()

def separar_codigos():
    # Consulta SQL para obter o nome do arquivo e o id da mesa
    consulta = """
    SELECT TABELA_CODIGO.arquivo, TABELA_MESA.idMesa
    FROM TABELA_CODIGO
    JOIN CODIGO_MESA ON TABELA_CODIGO.idCodigo = CODIGO_MESA.idCodigo
    JOIN TABELA_MESA ON CODIGO_MESA.idMesa = TABELA_MESA.idMesa
    WHERE TABELA_MESA.status = 1"""

    # Executar a consulta
    cursor.execute(consulta)

    # Fetchall para obter todos os resultados
    resultados = cursor.fetchall()

    # Criar lista com idMesa e arquivo
    lista_id_arquivo = [(idMesa, arquivo) for arquivo, idMesa in resultados]

    return lista_id_arquivo

def verificar_codigos_em_mesa(lista_id_codigos):
    # Consulta SQL para verificar se algum dos códigos está em uma mesa com status 1
    query = """
        SELECT COUNT(*) FROM CODIGO_MESA
        INNER JOIN TABELA_MESA ON CODIGO_MESA.idMesa = TABELA_MESA.idMesa
        WHERE CODIGO_MESA.idCodigo IN ({}) AND TABELA_MESA.status = 1
    """.format(','.join(['?'] * len(lista_id_codigos)))

    # Executar a consulta
    cursor.execute(query, lista_id_codigos)
    count = cursor.fetchone()[0]

    # Se count for maior que 0, significa que pelo menos um código está em uma mesa com status 1
    return count > 0

def alterar_status_mesa(id_mesa):
    try:
        # Executando a atualização
        cursor.execute("UPDATE TABELA_MESA SET status = 0 WHERE idMesa = ?", (id_mesa,))
        
        # Commitando a transação
        conn.commit()
        
        return True  # Retorna True se a atualização for bem-sucedida
    except sqlite3.Error as e:
        return e  # Retorna False se ocorrer algum erro