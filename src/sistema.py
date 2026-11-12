import csv
#Carregar os dados do arquivo CSV
def carregar_ocorrencias(caminho_arquivo):
    ocorrencias = []
    with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
        leitor = csv.DictReader(arquivo)
        for linha in leitor:
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
dados_validos, dados_invalidos = separar_ocorrencias(dados)

for item in dados_invalidos:
    print(item["ocorrencia"]["id"], "-", item["erros"])