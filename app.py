from flask import Flask, request   # Flask para criar a API, request para pegar dados da requisição
from flask_cors import CORS  # CORS para permitir requisições de outros domínios
import json  # JSON para ler e gravar dados em formato JSON

#intancia do flask
app = Flask("Cadastro de CPF")

# Ativando o CORS no aplicativo, permitindo que outras origens acessem a API.
CORS(app)

# Rota para consultar um cadastro a partir de um documento (CPF)
@app.route("/buscaCliente", methods=["GET"])
def buscaCliente():
    documento = request.args.get("doc")  # Pega o parâmetro 'doc' da URL
    print(documento)
    registro = clientes(documento)  # Chama a função 'dados' passando o CPF (documento)
    return registro  # Retorna o registro do cliente

@app.route("/salvar_cliente", methods=['POST'])
def salvar_cliente():
    novo_cliente = request.get_json()  # Obtém os dados do novo cliente no formato JSON
    cpf = novo_cliente.get('cpf')
    
    # Carrega os dados existentes
    dados_pessoas = carregar_arquivo()
    
    # Verifica se o CPF já está cadastrado
    if cpf in dados_pessoas:
        return json.dumps({"message": "CPF já existe"}), 400  # Retorna erro se o CPF já existir
    
    # Caso contrário, salva o novo cliente
    dados_pessoas[cpf] = novo_cliente
    gravar_arquivo(dados_pessoas)
    return json.dumps({"message": "Cliente salvo com sucesso!"}), 400

# Função para carregar os dados do arquivo JSON
def carregar_arquivo():
    # Caminho do arquivo JSON (cuidado, pode ser necessário ajustar o caminho dependendo do sistema operacional)
    caminho_arquivo =  "data\clientes.json"
    
    try:
        # Tentando abrir e carregar o arquivo JSON
        with open(caminho_arquivo, "r") as arq:
            return json.load(arq)  # Retorna o conteúdo do arquivo como um dicionário Python
    except Exception as e:
        return "Falha ao carregar o arquivo"  # Caso ocorra algum erro, retorna uma mensagem de erro

# Função para gravar dados no arquivo JSON
def gravar_arquivo(clientes_ordenados):
    clientes_ordenados = {k: v for k, v in sorted(clientes_ordenados.items(), key=lambda item: item[1]['nome'].lower())}
    print(clientes_ordenados)
    # Mesmo caminho do arquivo JSON
    caminho_arquivo = "data\clientes.json"
    
    try:
        # Tentando abrir o arquivo em modo de escrita
        with open(caminho_arquivo, "w") as arq:
            # Gravando os dados no arquivo com indentação para ficar mais legível
            json.dump(clientes_ordenados, arq, indent=4)
            return "dados armazenados"  # Retorna uma mensagem de sucesso
    except Exception:
        return "Falha ao carregar o arquivo"  # Retorna uma mensagem de erro caso falhe
    


# Função para salvar dados de um cliente (a partir do CPF)
def salvar_dados(cpf, registro):
    dados_pessoas = carregar_arquivo()  # Carrega os dados existentes no arquivo JSON
    dados_pessoas[cpf] = registro  # Adiciona ou atualiza o registro do cliente usando o CPF como chave
    gravar_arquivo(dados_pessoas)  # Grava os dados atualizados de volta no arquivo JSON

# Função para buscaClienter os dados de um cliente a partir do CPF
def clientes(cpf):
    dados_pessoas = carregar_arquivo()  # Carrega os dados do arquivo
    vazio = {
        "nome": "não encontrado",
        "data_nascimento": "não encontrado",
        "email": "não encontrado"
    }
    # Tenta pegar o registro do cliente a partir do CPF, se não encontrar, retorna um dicionário vazio
    print(dados_pessoas)
    print(type(dados_pessoas))
    cliente = dados_pessoas.get(cpf, vazio)
    return cliente  # Retorna os dados do cliente ou a mensagem de "não encontrado"

# Rodando o servidor Flask
if __name__ == "__main__":
    app.run(debug=True)  # Inicia o servidor em modo de debug

    # Exemplo de como salvar dados no arquivo JSON
    valores = {
        "nome": "Adolfo Silveira",
        "data_nascimento": "2000-05-03",
        "email": "adolfo.silveira@example.com"
    }
    salvar_dados("11111", valores)  # Salva um exemplo de dados com o CPF "11111"