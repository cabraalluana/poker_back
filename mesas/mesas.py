# Importa as bibliotecas necessárias
import random
import math
import shutil
import os
from mesas import bdMesas  # Importa o módulo bdMesas
from prettytable import PrettyTable

def encontrar_n(num_jogadores):
    """
    Esta função encontra o valor de 'n' para distribuir jogadores em mesas de forma equilibrada
    :param num_jogadores: Número total de jogadores
    :return: O valor de 'n' encontrado ou None se não for possível dividir equilibradamente
    """
    if num_jogadores <= 10:
        return 1
    elif num_jogadores % 10 == 0:
        return int(num_jogadores / 10)
    else:
        for n in range(2, num_jogadores):
            if (num_jogadores / n) > 3 and (num_jogadores/n) <= 10:
                return n
    return None

def numeroJogadoresMesa(numero_jogadores):
    """
    Esta função distribui os jogadores em mesas de forma equilibrada
    :param numero_jogadores: Número total de jogadores
    :return: Lista com a quantidade de jogadores em cada mesa
    """
    n = encontrar_n(numero_jogadores)
    jogadoresRestantes = numero_jogadores

    while jogadoresRestantes > numero_jogadores % n:
        qtdJogadoresMesas = []

        for i in range(n):
            qtdJogadoresMesas.append(math.floor(numero_jogadores / n))
            jogadoresRestantes = jogadoresRestantes - qtdJogadoresMesas[i]

    sobra = jogadoresRestantes
    for i in range(0, sobra):
        qtdJogadoresMesas[i] = qtdJogadoresMesas[i] + 1
        jogadoresRestantes = jogadoresRestantes - 1

    print("=====================================================================")
    print("mesa\tQuantidade de jogadores")
    for i in range(len(qtdJogadoresMesas)):
        print(f"{i + 1}\t{qtdJogadoresMesas[i]}")

    return qtdJogadoresMesas

def sortear_mesas(num_jogadores, listaIDs):
    """
    Esta função distribui jogadores aleatoriamente em mesas e exibe a distribuição
    :param num_jogadores: Número total de jogadores
    :param listaIDs: Lista de IDs de jogadores
    :return: Lista de listas contendo os idCodigo em cada mesa
    """
    num_jogadores_por_mesa = numeroJogadoresMesa(num_jogadores)
    num_mesas = len(num_jogadores_por_mesa)

    random.shuffle(listaIDs)

    tabela = {}
    indice_jogador = 0
    id_codigos_mesas = []  # Lista para armazenar os idCodigo em cada mesa

    for mesa in range(1, num_mesas + 1):
        num_jogadores = num_jogadores_por_mesa[mesa - 1]
        jogadores_na_mesa = []

        for _ in range(num_jogadores):
            jogadores_na_mesa.append(listaIDs[indice_jogador])
            id_codigos_mesas.append(listaIDs[indice_jogador])  # Adiciona o idCodigo à lista
            indice_jogador += 1

        tabela[mesa] = jogadores_na_mesa

    print("=====================================================================")
    print("mesa\tjogadores")
    for mesa, jogadores_na_mesa in tabela.items():
        print(f"{mesa}\t{jogadores_na_mesa}")

    # Retornar o vetor com as linhas da coluna 2 da tabela
    return [jogadores_na_mesa for jogadores_na_mesa in tabela.values()]

def criar_mesa_e_vincular_codigos(listas_de_codigos):
    bdMesas.criar_mesa_e_vincular_codigos(listas_de_codigos)  # Chamada à função do módulo bdMesas

# Definir a função para obter os IDs das mesas
def obter_id_mesas():
    # Utilizar uma list comprehension para extrair o primeiro elemento de cada linha
    # obtida da função bdMesas.obter_id_mesas()
    id_mesas = [linha[0] for linha in bdMesas.obter_id_mesas()]

    # Retornar a lista de IDs das mesas
    return id_mesas

def consultar_mesas_e_codigos(id_mesas):
    # Criar uma tabela
    tabela = PrettyTable()
    
    # Definir os nomes das colunas da tabela
    tabela.field_names = ["idMesa", "idCodigo", "nome"]
    
    # Obter os dados do banco de dados usando a função bdMesas.consultar_mesas_e_codigos
    for tupla in bdMesas.consultar_mesas_e_codigos(id_mesas):
        # Iterar sobre os resultados da consulta
        for resultado in tupla:
            # Adicionar uma linha à tabela para cada resultado
            tabela.add_row([resultado[0], resultado[1], resultado[2]])

    # Imprimir a tabela formatada
    print(tabela)

def criar_pastas_mesas_ativas():
    bdMesas.criar_pastas_mesas_ativas()

def separar_codigos():
    return bdMesas.separar_codigos()

def dividir_codigo_mesas(lista_arquivos):
    # Percorre a lista de arquivos
    for id_mesa, nome_arquivo in lista_arquivos:
        # Diretório de origem do arquivo
        origem = f"arquivos/{nome_arquivo}"
        # Diretório de destino da mesa
        destino = f"mesas_ativas/mesa_{id_mesa}"
        
        # Verifica se o diretório de destino existe, se não, cria-o
        if not os.path.exists(destino):
            os.makedirs(destino)
        
        # Move o arquivo para o diretório de destino
        shutil.move(origem, destino)

def mover_arquivos(id_mesa):
    # Definindo os caminhos das pastas
    pasta_origem = f"mesas_ativas/mesa_{id_mesa}"
    pasta_destino = "AIs"
    
    # Verificando se a pasta de origem existe
    if not os.path.exists(pasta_origem):
        print(f"A pasta {pasta_origem} não existe.")
        return
    
    # Verificando se a pasta de destino existe, se não, criando-a
    if not os.path.exists(pasta_destino):
        os.makedirs(pasta_destino)
    
    # Apagando todos os arquivos na pasta de destino
    for arquivo in os.listdir(pasta_destino):
        arquivo_path = os.path.join(pasta_destino, arquivo)
        try:
            if os.path.isfile(arquivo_path):
                os.unlink(arquivo_path)
        except Exception as e:
            print(f"Erro ao apagar {arquivo_path}: {e}")
    
    # Movendo os arquivos da pasta de origem para a pasta de destino
    for arquivo in os.listdir(pasta_origem):
        arquivo_path_origem = os.path.join(pasta_origem, arquivo)
        arquivo_path_destino = os.path.join(pasta_destino, arquivo)
        try:
            shutil.move(arquivo_path_origem, arquivo_path_destino)
        except Exception as e:
            print(f"Erro ao mover {arquivo_path_origem} para {arquivo_path_destino}: {e}")
    
    print("Arquivos movidos com sucesso!")