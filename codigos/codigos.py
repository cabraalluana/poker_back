# Importa o módulo bdCodigos da biblioteca codigos
from codigos import bdCodigos
# Importa a biblioteca JSON para lidar com dados em formato JSON
import json

def enviarArquivo(idUsuario):
    """
    Esta função salva o código enviado no banco de dados
    :param idUsuario: O ID do usuário que está enviando o código
    """
    idUsuario = '{:04d}'.format(idUsuario)
    arquivo = 'c2023_' + str(idUsuario) + '.m'
    
    # Chama a função salvarCodigo do módulo bdCodigos para salvar o código no banco de dados
    bdCodigos.salvarCodigo(arquivo, idUsuario)
    print("=====================================================================")
    print("Código enviado com sucesso!")

def numeroJogadores():
    """
    Esta função retorna o número de jogadores que enviaram códigos
    :return: Número de jogadores
    """
    return bdCodigos.numeroJogadores()

def listaIDs():
    """
    Esta função retorna uma lista de IDs dos códigos enviados
    :return: Lista de IDs dos códigos
    """
    return bdCodigos.listaIDs()

def apagarCodigo(idCodigo, idUsuario):
    """
    Esta função apaga um código específico enviado por um usuário
    :param idCodigo: O ID do código a ser apagado
    :param idUsuario: O ID do usuário que enviou o código
    """
    if bdCodigos.apagarCodigo(idCodigo, idUsuario):
        print("=====================================================================")
        print("Código apagado com sucesso.")
    else:
        print("=====================================================================")
        print("Não foi possível apagar o código informado.")

def codigosEnviados(dados_usuario_desejado):
    """
    Esta função retorna uma lista de IDs dos códigos enviados por um usuário específico
    :param dados_usuario_desejado: Uma tupla contendo o ID e o nome do usuário desejado
    """
    codigos_do_usuario = bdCodigos.codigosEnviados(dados_usuario_desejado[0])

    print("=====================================================================")

    if codigos_do_usuario:
        print(f"IDs dos códigos enviados por {dados_usuario_desejado[1]}")
        for codigo in codigos_do_usuario:
            print(f"{codigo}")
    else:
        print(f"Não foram encontrados códigos enviados por {dados_usuario_desejado[1]}.")

def apagar_linha_por_id_usuario(id_usuario):
    return bdCodigos.apagar_linha_por_id_usuario(id_usuario)