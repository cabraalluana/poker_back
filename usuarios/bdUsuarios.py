import sqlite3 

# Conecta ao banco de dados SQLite (ou cria se não existir)
conn = sqlite3.connect('bdPoker.db')
conn.execute('PRAGMA encoding = "UTF-8"')

# Cria um cursor para executar comandos SQL
cursor = conn.cursor()

# Cria a tabela 'TABELA_USUARIO' se ela não existir
cursor.execute("""
               CREATE TABLE IF NOT EXISTS TABELA_USUARIO (
               "idUsuario"	INTEGER NOT NULL UNIQUE,
               "nome"	TEXT NOT NULL,
               "email"	TEXT NOT NULL UNIQUE,
               "senha"	TEXT NOT NULL,
               PRIMARY KEY("idUsuario" AUTOINCREMENT)
               );
               """)

def salvarUsuario(nome, email, senha):
    """Esta função salva o usuário no banco de dados"""
    cursor.execute("""
                   INSERT INTO TABELA_USUARIO(nome, email, senha) VALUES(?, ?, ?)
                   """, (nome, email, senha))
    
    conn.commit()

def verificarUsuario(email, senha):
    """Esta função consulta se existe o usuário no banco de dados"""
    cursor.execute("""SELECT * FROM TABELA_USUARIO
                   WHERE (email = ? and senha = ?)
                   """, (email, senha))
    
    verifyLogin = cursor.fetchone()
    try:
        if (email in verifyLogin and senha in verifyLogin):
            return True
    except:
        return False
    
def existeEmail(email):
    """Esta função verifica se o email informado no cadastro já existe"""
    cursor.execute("""SELECT * FROM TABELA_USUARIO
                   WHERE (email = ?)
                   """, (email,))
    
    verifyEmail = cursor.fetchone()
    if verifyEmail:
        return True
    else:
        return False
    
def consultaUsuario(email):
    """Esta função retorna o ID do usuário"""
    cursor.execute("""SELECT * FROM TABELA_USUARIO
                   WHERE (email = ?)
                   """, (email,))
    
    return cursor.fetchone()

def imprimirTabelaUsuario():
    # Executar consulta SQL para selecionar idUsuario, nome e email da TABELA_USUARIO
    cursor.execute("SELECT idUsuario, nome, email FROM TABELA_USUARIO")

    # Recuperar os resultados
    return cursor.fetchall()

def editarPerfilUsuario(campos_editar, idUsuario):
    # Atualizar os campos escolhidos
    for campo, valor in campos_editar:
        cursor.execute(f"UPDATE TABELA_USUARIO SET {campo} = ? WHERE idUsuario = ?", (valor, idUsuario))

    conn.commit()

def usuarioExiste(idUsuario):
    # Verificar se o usuário existe
    cursor.execute("SELECT nome FROM TABELA_USUARIO WHERE idUsuario = ?", (idUsuario,))
    
    return cursor.fetchone()

def apagarContaUsuario(idUsuario):
    # Excluir a conta do usuário
    cursor.execute("DELETE FROM TABELA_USUARIO WHERE idUsuario = ?", (idUsuario,))
    conn.commit()
        