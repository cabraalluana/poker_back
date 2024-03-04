# Importa os módulos necessários
from usuarios import usuarios
from codigos import codigos
from mesas import mesas
from resultados import resultados
import getpass

def main():
    # Loop principal do programa
    while True:
        print("=====================================================================")
        print("Início")
        print("1 - Usuário;")
        print("2 - Mesas;")
        print("0 - Sair.")

        # Solicitar a escolha do usuário
        escolha = int(input("Escolha uma opção: "))

        # Realizar ações com base na escolha
        if escolha == 1:
            areaUsuario()
        elif escolha == 2:
            areaMesas()
        elif escolha == 0:
            # Fechar conexões e encerrar o programa
            usuarios.bdUsuarios.conn.close()
            codigos.bdCodigos.conn.close()
            mesas.bdMesas.conn.close()
            resultados.bdResultados.conn.close()
            break
        else:
            print("=====================================================================")
            print("Escolha uma opção válida")

def areaUsuario():
    # Loop da área do usuário
    while True:
        print("=====================================================================")
        print("Área do usuário")
        print("1 - Cadastrar;")
        print("2 - Login;")
        print("3 - Ver todos usuários;")
        print("0 - Sair da área do usuário.")

        # Solicitar a escolha do usuário na área do usuário
        escolhaUsuario = int(input("Escolha uma opção: "))
        if escolhaUsuario == 1:
            usuarios.salvarArquivo()
        elif escolhaUsuario == 2:
            # Realizar login
            print("=====================================================================")
            email = input("Email:")
            senha = getpass.getpass(prompt="Senha: ")
            
            # Verificar o usuário e proceder com o login se válido
            if usuarios.verificarUsuario(email, senha):
                usuarioLogado(email)
        elif escolhaUsuario == 3:
            # Visualizar todos os usuários
            usuarios.imprimirTabelaUsuario()
        elif escolhaUsuario == 0:
            break
        else:
            print("=====================================================================")
            print("Escolha uma opção válida")

def usuarioLogado(email):
    # Obter dados do usuário logado
    dadosUsuario = usuarios.consultaUsuario(email)
    dadosUsuario = list(dadosUsuario)
    dadosUsuario[1] = dadosUsuario[1]
    dadosUsuario = tuple(dadosUsuario)

    # Loop para as opções do usuário logado
    while True:
        print("=====================================================================")
        print(f"{dadosUsuario[1]}")
        print("1 - Códigos;")
        print("2 - Editar dados;")
        print("3 - Apagar conta;")
        print("0 - Sair do perfil.")

        # Solicitar a escolha do usuário logado
        escolhaUsuario = int(input("Escolha uma opção: "))
        if escolhaUsuario == 1:
            areaCodigos(dadosUsuario)
        elif escolhaUsuario == 2:
            # Editar perfil do usuário
            novo_email = usuarios.editarPerfilUsuario(dadosUsuario)
            dadosUsuario = usuarios.consultaUsuario(novo_email)

            dadosUsuario = list(dadosUsuario)
            dadosUsuario[1] = dadosUsuario[1].encode('latin-1').decode('utf-8')
        elif escolhaUsuario == 3:
            # Apagar conta do usuário e seus códigos
            if mesas.verificar_codigos_em_mesa(codigos.codigosEnviados(dadosUsuario)):
                print(f"Usuário {dadosUsuario[1]} está em uma partida ativa.")
            else:
                if usuarios.apagarContaUsuario(dadosUsuario[0]) and codigos.apagar_linha_por_id_usuario(dadosUsuario[0]):
                    break
        elif escolhaUsuario == 0:
            break
        else:
            print("=====================================================================")
            print("Escolha uma opção válida")

def areaCodigos(dadosUsuario):
    # Loop da área de códigos
    while True:
        print("=====================================================================")
        print("Códigos")
        print("1 - Enviar código;")
        print("2 - Visualizar envios;")
        print("3 - Editar dados;")
        print("4 - Apagar envio;")
        print("0 - Sair da área de códigos.")

        # Solicitar a escolha da área de códigos
        escolhaCodigo = int(input("Escolha uma opção: "))
        if escolhaCodigo == 1:
            # Enviar código
            codigos.enviarArquivo(dadosUsuario[0])
        elif escolhaCodigo == 2:
            # Visualizar códigos enviados
            codigos.codigosEnviados(dadosUsuario)
        elif escolhaCodigo == 3:
            print("=====================================================================")
            print("Esta função não foi feita")
        elif escolhaCodigo == 4:
            # Apagar código enviado
            codigos.codigosEnviados(dadosUsuario)
            print("=====================================================================")
            idCodigo = int(input("Informe o ID do código que deseja apagar ou aperte 0 para voltar para a área do usuário: "))
            if idCodigo > 0:
                codigos.apagarCodigo(idCodigo, dadosUsuario[0])
            elif idCodigo < 0:
                print("=====================================================================")
                print("Código inválido")
        elif escolhaCodigo == 0:
            break
        else:
            print("=====================================================================")
            print("Escolha uma opção válida")

def areaMesas():
    # Loop da área de mesas
    while True:
        print("=====================================================================")
        print("Área das mesas")
        print("1 - Separar mesas;")
        print("2 - Listar mesas ativas")
        print("3 - Listar mesas inativas")
        print("4 - Rodar mesas")
        print("0 - Sair da área das mesas.")
        
        # Solicitar a escolha da área de mesas
        escolha = int(input("Escolha uma opção: "))

        # Realizar ações com base na escolha
        if escolha == 1:
            # Separar mesas e vincular códigos
            if codigos.numeroJogadores() == 0:
                print("Todos os jogadores estão em uma partida.")
            else:
                res = mesas.sortear_mesas(codigos.numeroJogadores(), codigos.listaIDs())
                mesas.criar_mesa_e_vincular_codigos(res)
        elif escolha == 2:
            print("=====================================================================")
            id_mesas = mesas.obter_id_mesas(1)
            mesas.consultar_mesas_e_codigos(id_mesas, 1)
        elif escolha == 3:
            print("=====================================================================")
            id_mesas = mesas.obter_id_mesas(0)
            mesas.consultar_mesas_e_codigos(id_mesas, 0)
        elif escolha == 4:
            print("=====================================================================")
            mesas.criar_pastas_mesas_ativas()
            print("Pastas das mesas ativas criadas com sucesso!")
            print("=====================================================================")
            lista_id_arquivo = mesas.separar_codigos()
            mesas.dividir_codigo_mesas(lista_id_arquivo)
            print("Arquivos movidos com sucesso!")
            print("=====================================================================")
            while True:
                print("1 - Rodar mesa")
                print("0 - Voltar da área das mesas.")
                # Solicitar a escolha da área de mesas
                escolha = int(input("Escolha uma opção: "))
                print("=====================================================================")

                if escolha == 1:
                    id_mesa = input("Informe o ID da mesa: ")
                    print("=====================================================================")
                    # Chamando a função para modificar o dataframe
                    df_resultados = resultados.resultado_mesa(resultados.ler_csv_para_dataframe(), mesas.mover_arquivos(id_mesa))
                    mesas.alterar_status_mesa(id_mesa)
                    resultados.salvar_resultado(df_resultados, id_mesa)
                elif escolha == 0:
                    break
                else:
                    print("=====================================================================")
                    print("Escolha uma opção válida")
        elif escolha == 0:
            break
        else:
            print("=====================================================================")
            print("Escolha uma opção válida")

# Iniciar o programa
if __name__ == '__main__':
    main()