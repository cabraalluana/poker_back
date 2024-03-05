# Configurando o Ambiente

## Preparando o ambiente Python:
- Antes de tudo, certifique-se de ter o Python instalado. Caso contrário, você pode baixá-lo [aqui](https://www.python.org/downloads/release/python-3106/).

## Instalação do Virtual Environment:
- Utilizaremos um ambiente virtual chamado "virtualenv". Você pode instalá-lo executando o seguinte comando no terminal:
  ```
  pip install virtualenv
  ```

# Carregando o Projeto Localmente

1. Selecione o botão verde "Code" no canto superior direito do repositório no GitHub.
2. Na aba "HTTPS", copie a URL do GitHub.
3. Abra o terminal na pasta desejada e execute o seguinte comando para clonar o repositório:
   ```
   git clone <link_do_repositório>
   ```

# Rodando a Aplicação

Para executar a aplicação, siga estes passos:

1. Abra um novo terminal na IDE do Visual Studio Code (Ctrl+J).
2. Crie um ambiente virtual na pasta do projeto executando o seguinte comando:
   - **Windows**:
      ```
      python -m virtualenv .venv
      ```
      ou
      ```
      python -m venv .venv
      ```
   - **Linux/macOS**:
      ```
      python3 -m venv .venv
      ```

3. Ative o ambiente virtual. Dependendo do seu sistema operacional, você pode precisar executar o seguinte comando:
   - **Windows**:
     ```
     .venv\Scripts\activate
     ```
     Se o comando acima não funcionar devido à execução de scripts estar desabilitada, execute o seguinte comando antes e tente novamente:
     ```
     Set-ExecutionPolicy RemoteSigned -Scope Process
     ```

   - **Linux/macOS**:
     ```
     source .venv/bin/activate
     ```

4. Após ativar o ambiente virtual, você verá "(.venv)" antes do prompt de comando, indicando que está ativado.

5. Instale todas as dependências listadas no arquivo "requirements.txt" executando o seguinte comando:
   ```
   pip install -r requirements.txt
   ```

6. Agora você está pronto para iniciar a aplicação! Para executar o programa, basta digitar o seguinte comando no terminal:
   - **Windows**:
      ```
      python main.py
      ```
   - **Linux/macOS**:
      ```
      python3 main.py
      ```

# Observações

- Lembre-se sempre de ativar o ambiente virtual ao abrir uma nova sessão no Visual Studio Code;
- Após instalar novas dependências, não se esqueça de atualizar o arquivo "requirements.txt" executando o comando `pip freeze > requirements.txt` para manter o arquivo atualizado.