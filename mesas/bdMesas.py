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

def criar_pastas_mesas_ativas(caminho_pasta):
    # Consulta para selecionar idCodigo e status da tabela
    cursor.execute("SELECT idMesa, status FROM TABELA_MESA")

    # Iterar sobre os resultados
    for row in cursor.fetchall():
        idCodigo, status = row
        if status == 'ativo':
            # Criar o nome da pasta
            nome_pasta = f'mesa_{idCodigo}'
            
            # Caminho completo da pasta
            caminho_completo = os.path.join(caminho_pasta, nome_pasta)
            
            # Verificar se a pasta não existe antes de criar
            if not os.path.exists(caminho_completo):
                os.makedirs(caminho_completo)

def separar_codigos():
    # Consulta SQL para obter o nome do arquivo e o id da mesa
    consulta = """
    SELECT TC.arquivo, CM.idMesa
    FROM CODIGO_MESA CM
    JOIN TABELA_CODIGO TC ON CM.idCodigo = TC.idCodigo;
    """

    # Executar a consulta
    cursor.execute(consulta)

    # Fetchall para obter todos os resultados
    resultados = cursor.fetchall()

    # Criar lista com idMesa e arquivo
    lista_id_arquivo = [(idMesa, arquivo) for arquivo, idMesa in resultados]

    return lista_id_arquivo