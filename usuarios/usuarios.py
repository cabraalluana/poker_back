# Importa o módulo necessário para acessar o banco de dados de usuários
from usuarios import bdUsuarios
import json
from prettytable import PrettyTable

def salvarArquivo():
    """Esta função lê o arquivo de novos usuarios.json e salva no banco de dados"""

    # Abre o arquivo JSON e carrega os dados
    with open('json/usuarios.json', 'r') as arquivo_json:
        dados = json.load(arquivo_json)

    # Acessa a lista de pessoas no JSON
    pessoas = dados['pessoas']

    for pessoa in pessoas:
        nome = pessoa['nome']
        email = pessoa['email']
        senha = pessoa['senha']

    # Verifica se o email já existe na tabela de usuários
    if bdUsuarios.existeEmail(email) == False:
        # Tenta salvar o usuário no banco de dados
        retorno = bdUsuarios.salvarUsuario(nome, email, senha)
        if (retorno == False):
            print("=====================================================================")
            print("Não deixe nenhum campo vazio. Preencha todos os campos")
        else:
            print("=====================================================================")
            print("Conta criada com sucesso.")
    else:
        print("=====================================================================")
        print("O email já está sendo usado.")

    
def verificarUsuario(email, senha):
    """Esta função verifica se o usuário existe no banco de dados"""
    if bdUsuarios.verificarUsuario(email, senha):
        print("=====================================================================")
        print(f"Acesso confirmado. Olá, {consultaUsuario(email)[1]}!")
    else:
        print("=====================================================================")
        print("Acesso negado. Verifique se está cadastrado no sistema!")
    return bdUsuarios.verificarUsuario(email, senha)

def consultaUsuario(email):
    """Esta função retorna o ID do usuário"""
    return bdUsuarios.consultaUsuario(email)

def imprimirTabelaUsuario():
    resultados = bdUsuarios.imprimirTabelaUsuario()
    # Verificar se há dados
    if not resultados:
        print("Nenhum dado encontrado na tabela TABELA_USUARIO.")
        return

    # Criar uma tabela formatada
    tabela = PrettyTable()
    tabela.field_names = ["ID do Usuário", "Nome", "E-mail"]

    # Adicionar os dados à tabela
    for idUsuario, nome, email in resultados:
        tabela.add_row([idUsuario, nome, email])

    # Imprimir a tabela
    print(tabela)

def editarPerfilUsuario(dadosUsuario):
    # Exibir os dados atuais do usuário
    print("=====================================================================")
    print(f"Dados atuais:")
    print(f"Nome: {dadosUsuario[1]}")
    print(f"Email: {dadosUsuario[2]}")

    # Solicitar ao usuário quais campos deseja editar
    campos_editar = []
    novo_email = None  # Declare novo_email como None no início

    while True:
        print("=====================================================================")
        opcao = input("Deseja editar o nome (N) ou o email (E)? Ou digite 'S' para sair: ").strip().upper()
        if opcao == 'N':
            print("=====================================================================")
            novo_nome = input("Digite o novo nome: ")
            campos_editar.append(('nome', novo_nome))
        elif opcao == 'E':
            print("=====================================================================")
            novo_email = input("Digite o novo email: ")
            campos_editar.append(('email', novo_email))
        elif opcao == 'S':
            break
        else:
            print("=====================================================================")
            print("Opção inválida. Tente novamente.")

    bdUsuarios.editarPerfilUsuario(campos_editar, dadosUsuario[0])

    print("=====================================================================")
    print("Dados atualizados com sucesso.")

    if novo_email:
        return novo_email
    else:
        return dadosUsuario[2]

def apagarContaUsuario(idUsuario):
    usuario = bdUsuarios.usuarioExiste(idUsuario)

    if usuario is None:
        print("Usuário não encontrado.")
        return

    nome_usuario = usuario[0]

    # Solicitar confirmação do usuário
    print("=====================================================================")
    confirmacao = input(f"Tem certeza de que deseja apagar a conta de {nome_usuario}? (S/N): ").strip().upper()

    if confirmacao == 'S':
        bdUsuarios.apagarContaUsuario(idUsuario)
        print("=====================================================================")
        print("Conta apagada com sucesso.")
        return True
    else:
        print("=====================================================================")
        print("Operação cancelada.")
        return False