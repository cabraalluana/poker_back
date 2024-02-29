import pandas as pd
from resultados import bdResultados

def ler_csv_para_dataframe():
    # Lê o arquivo CSV e cria um dataframe
    df_resultados = pd.read_csv("resultados.csv")
    return df_resultados

def resultado_mesa(df_resultados, arquivos):
    # Atualize o nome do jogador com o nome do arquivo correspondente
    for i, jogador in enumerate(df_resultados['Jogador']):
        numero = int(jogador[5:])  # Extrai o número do nome do jogador
        nome_arquivo = arquivos[numero - 1]  # Obtém o nome do arquivo correspondente
        df_resultados.at[i, 'Jogador'] = nome_arquivo

    return df_resultados

def salvar_resultado(df_resultado, idMesa):
    # Obtém os jogadores de cada posição
    primeiro_lugar = df_resultado.iloc[0]['Jogador']
    segundo_lugar = df_resultado.iloc[1]['Jogador']
    terceiro_lugar = df_resultado.iloc[2]['Jogador']

    bdResultados.salvar_resultado(idMesa, primeiro_lugar, segundo_lugar, terceiro_lugar)