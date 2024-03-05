# Importa a biblioteca SQLite
import sqlite3

# Conectar ao banco de dados
conn = sqlite3.connect('bdPoker.db')

# Define a codificação UTF-8 para o banco de dados
conn.execute('PRAGMA encoding = "UTF-8"')

# Cria um cursor para executar comandos SQL
cursor = conn.cursor()

# Cria a tabela TABELA_CODIGO se não existir
cursor.execute("""
               CREATE TABLE IF NOT EXISTS TABELA_CODIGO (
               "idCodigo"    INTEGER NOT NULL UNIQUE,
               "arquivo"     TEXT NOT NULL,
               "idUsuario"   INTEGER NOT NULL UNIQUE,
               FOREIGN KEY("idUsuario") REFERENCES "TABELA_USUARIO"("idUsuario"),
               PRIMARY KEY("idCodigo" AUTOINCREMENT)
               );
               """)

def salvarCodigo(arquivo, idUsuario):
    """
    Esta função apaga o código existente do usuário (se houver) e adiciona o novo código para a 
    competição no banco de dados
    :param arquivo: O conteúdo do código a ser salvo
    :param idUsuario: O ID do usuário que está enviando o código
    """
    # Primeiro, apagar o código existente do usuário, se houver
    cursor.execute("""
                   DELETE FROM TABELA_CODIGO WHERE idUsuario = ?
                   """, (idUsuario,))
    
    # Em seguida, inserir o novo código
    cursor.execute("""
                   INSERT INTO TABELA_CODIGO(arquivo, idUsuario) VALUES(?, ?)
                   """, (arquivo, idUsuario))
    
    # Commit para salvar as alterações no banco de dados
    conn.commit()

def numeroJogadores():
    """
    Esta função retorna o número de jogadores que enviaram códigos que não estão em uma mesa com status ativa.
    :return: Número de jogadores
    """
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

    return cursor.fetchone()[0]

def listaIDs():
    """
    Esta função retorna uma lista de IDs dos códigos enviados
    :return: Lista de IDs dos códigos
    """
    cursor.execute("""SELECT idCodigo
                   FROM TABELA_CODIGO
                   WHERE idCodigo NOT IN (
                        SELECT idCodigo
                        FROM CODIGO_MESA
                        INNER JOIN TABELA_MESA ON CODIGO_MESA.idMesa = TABELA_MESA.idMesa
                        WHERE TABELA_MESA.status = '1')
                   """)

    # Obtém os IDs dos códigos como uma lista
    id_codigo_list = [row[0] for row in cursor.fetchall()]

    return id_codigo_list

def apagarCodigo(idCodigo, idUsuario):
    """
    Esta função apaga um código específico enviado por um usuário
    :param idCodigo: O ID do código a ser apagado
    :param idUsuario: O ID do usuário que enviou o código
    :return: True se o código foi apagado com sucesso, False caso contrário
    """
    # Verifica se o código pertence ao usuário antes de apagar
    cursor.execute('SELECT COUNT(*) FROM TABELA_CODIGO WHERE idCodigo = ? and idUsuario = ?', (idCodigo, idUsuario))
    count = cursor.fetchone()[0]

    if count == 0:
        return False
    
    # Apaga o código da tabela
    cursor.execute('DELETE FROM TABELA_CODIGO WHERE idCodigo = ? and idUsuario = ?', (idCodigo, idUsuario))

    # Commit para salvar as alterações no banco de dados
    conn.commit()

    try:
        return True
    except:
        return False

def codigosEnviados(id_usuario_desejado):
    """
    Esta função retorna uma lista de IDs dos códigos enviados por um usuário específico
    :param id_usuario_desejado: O ID do usuário desejado
    :return: Lista de IDs dos códigos enviados pelo usuário
    """

    # Obtém os IDs dos códigos enviados pelo usuário
    cursor.execute('SELECT idCodigo FROM TABELA_CODIGO WHERE idUsuario = ?', (id_usuario_desejado,))
    codigos_do_usuario = [row[0] for row in cursor.fetchall()]

    return codigos_do_usuario

def apagar_linha_por_id_usuario(id_usuario):
    """
    Esta função apaga todas as linhas relacionadas a um usuário na tabela TABELA_CODIGO
    :param id_usuario: O ID do usuário
    :return: True se as linhas foram apagadas com sucesso, False caso contrário
    """
    try:
        # Apaga todas as linhas relacionadas ao usuário na tabela
        cursor.execute("DELETE FROM TABELA_CODIGO WHERE idUsuario = ?", (id_usuario,))
        
        # Commit para salvar as alterações no banco de dados
        conn.commit()
        print(f"Códigos apagado para idUsuario {id_usuario}")
        return True
    except Exception as e:
        # Em caso de erro, desfaz as alterações
        conn.rollback()
        print(f"Erro ao apagar código: {e}")
        return False
