import sqlite3

def verificar_codigos_em_mesa(lista_id_codigos):
    # Conectar ao banco de dados
    conn = sqlite3.connect('bdPoker.db')
    cursor = conn.cursor()

    # Consulta SQL para verificar se algum dos códigos está em uma mesa com status 1
    query = """
        SELECT COUNT(*) FROM CODIGO_MESA
        INNER JOIN TABELA_MESA ON CODIGO_MESA.idMesa = TABELA_MESA.idMesa
        WHERE CODIGO_MESA.idCodigo IN ({}) AND TABELA_MESA.status = 1
    """.format(','.join(['?'] * len(lista_id_codigos)))

    # Executar a consulta
    cursor.execute(query, lista_id_codigos)
    count = cursor.fetchone()[0]

    # Fechar a conexão com o banco de dados
    conn.close()

    # Se count for maior que 0, significa que pelo menos um código está em uma mesa com status 1
    return count > 0

# Exemplo de uso
lista_codigos = [11, 32, 31]  # Substitua isso com a sua lista de idCodigo
resultado = verificar_codigos_em_mesa(lista_codigos)
print(resultado)
