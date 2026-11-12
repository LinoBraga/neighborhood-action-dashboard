import csv
#Carregar os dados do arquivo CSV
def carregar_ocorrencias(caminho_arquivo):
    ocorrencias = []
    with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
        leitor = csv.DictReader(arquivo)
        for linha in leitor:
            #data abertura e data de conclusão devem ser convertidas para inteiro, caso contrário, devem ser None
            if linha["data_abertura"] != "":
                linha["data_abertura"] = int(linha["data_abertura"])
            else:
                linha["data_abertura"] = None
            if linha["data_conclusao"] != "":
                linha["data_conclusao"] = int(linha["data_conclusao"])
            else:
                linha["data_conclusao"] = None
            ocorrencias.append(linha)
        return ocorrencias
dados = carregar_ocorrencias("data/ocorrencias.csv")

#verificar se a ocorrência é válida
def validar_ocorrencia(ocorrencia):
    erros = []

    categorias_validas = ["ILU", "ACE", "LIM", "CON"]
    status_validos = ["ABERTA", "EM_ANALISE", "CONCLUIDA"]

    if not ocorrencia["id"]:
        erros.append("ID não informado")

    if ocorrencia["categoria"] not in categorias_validas:
        erros.append("Categoria inválida")

    if not ocorrencia["descricao"]:
        erros.append("Descrição não informada")

    if not ocorrencia["localidade"]:
        erros.append("Localidade não informada")

    if ocorrencia["data_abertura"] is None:
        erros.append("Data de abertura inválida")

    if ocorrencia["status"] not in status_validos:
        erros.append("Status inválido")

    if ocorrencia["status"] == "CONCLUIDA":
        if ocorrencia["data_conclusao"] is None:
            erros.append("Ocorrência concluída sem data de conclusão")

    elif ocorrencia["data_conclusao"] is not None:
        erros.append("Ocorrência não concluída possui data de conclusão")

    return erros
for ocorrencia in dados:
    erros = validar_ocorrencia(ocorrencia)

    if erros:
        print(ocorrencia["id"], erros)

#Separar e tratar dados
def separar_ocorrencias(ocorrencias):
    dados_validos = []
    dados_invalidos = []
    for ocorrencia in ocorrencias:
        erros = validar_ocorrencia(ocorrencia)
        if erros:
            dados_invalidos.append({"ocorrencia": ocorrencia, "erros": erros})
        else:
            dados_validos.append(ocorrencia)
    print("Ocorrências válidas:", len(dados_validos))
    print("Ocorrências inválidas:", len(dados_invalidos))
    return dados_validos, dados_invalidos

#Criando indice de ocorrências para busca rápida
def criar_indice_ocorrencias(ocorrencias):
    indice = {}
    for ocorrencia in ocorrencias:
        id = ocorrencia["id"]
        indice[id] = ocorrencia
    return indice

#busca de ocorrências por ID, categoria e status
def buscar_por_id(indice, id):
    if id in indice:
        return indice[id]
    else:
        return None
    
def buscar_por_categoria(ocorrencias, categoria):
    resultados = []
    for ocorrencia in ocorrencias:
        if ocorrencia["categoria"] == categoria:
            resultados.append(ocorrencia)
    return resultados
def buscar_por_status(ocorrencias, status):
    resultados = []
    for ocorrencia in ocorrencias:
        if ocorrencia["status"] == status:
            resultados.append(ocorrencia)
    return resultados

#cadastrando ocorrências
def cadastrar_ocorrencia(ocorrencias):
    id_ocorrencia = input("Digite o ID da ocorrência: ")
    for ocorrencia in ocorrencias:
        if ocorrencia["id"] == id_ocorrencia:
            print("ID já cadastrado. Tente novamente.")
            return None
    categoria = input("Digite a categoria da ocorrência (ILU, ACE, LIM, CON): ")
    descricao = input("Digite a descrição da ocorrência: ")
    localidade = input("Digite a localidade da ocorrência: ")
    data_abertura = input("Digite a data de abertura da ocorrência: ")
    status = "ABERTA"
    data_conclusao = None

    ocorrencia = {
        "id": id_ocorrencia,
        "categoria": categoria,
        "descricao": descricao,
        "localidade": localidade,
        "data_abertura": int(data_abertura) if data_abertura else None,
        "status": status,
        "data_conclusao": int(data_conclusao) if data_conclusao else None
    }

    erros = validar_ocorrencia(ocorrencia)
    if erros:
        print("Ocorrência inválida:", erros)
        return None
    else:
        return ocorrencia
        ocorrencias.append(ocorrencia)
    

dados_validos, dados_invalidos = separar_ocorrencias(dados)

indice = criar_indice_ocorrencias(dados_validos)

resultado = buscar_por_id(indice, "OC007")

if resultado is not None:
    print("Ocorrência encontrada:")
    print(resultado)
else:
    print("Ocorrência não encontrada.")
resultado = buscar_por_categoria(dados_validos, "ILU")

print("Total encontrado:", len(resultado))

for ocorrencia in resultado:
    print(ocorrencia["id"], ocorrencia["descricao"])
resultado = buscar_por_status(dados_validos, "ABERTA")

print("Total de ocorrências abertas:", len(resultado))

for ocorrencia in resultado:
    print(ocorrencia["id"], ocorrencia["descricao"])