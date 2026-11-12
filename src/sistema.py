import csv
#fila de atendimento
fila_atendimento = []
#pilha

pilha_historico = []
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
    #Status inicial da ocorrência é sempre "ABERTA" e data de conclusão é None
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
        #Adcionando a ocorrência à lista de ocorrências
        ocorrencias.append(ocorrencia)
        return ocorrencia
    
#Alterando status de ocorrências 
def alterar_status(ocorrencias, id, novo_status):
    for ocorrencia in ocorrencias:
        if ocorrencia["id"] == id:
            if novo_status not in ["ABERTA", "EM_ANALISE", "CONCLUIDA"]:
                print("Status inválido. Tente novamente.")
                return False
            ocorrencia["status"] = novo_status
            if novo_status != "CONCLUIDA":
                ocorrencia["data_conclusao"] = None
            if novo_status == "CONCLUIDA":
                ocorrencia["data_conclusao"] = int(input("Digite a data de conclusão da ocorrência: "))
            return True
    return False

#Registrar histórico de alterações de status
def registrar_historico(ocorrencias, id, novo_status):
    for ocorrencia in ocorrencias:
        if ocorrencia["id"] == id:
            if "historico" not in ocorrencia:
                ocorrencia["historico"] = []
            ocorrencia["historico"].append({"status": novo_status, "data": int(input("Digite a data da alteração de status: "))})
            return True
    return False

#Listar histórico de alterações de status
def listar_historico(ocorrencias, id):
    for ocorrencia in ocorrencias:
        if ocorrencia["id"] == id:
            if "historico" in ocorrencia:
                return ocorrencia["historico"]
            else:
                return []
    return None

#Adicionar fila de ocorrencias. Retorne True se conseguir adicionar e False se não encontrar.
def adicionar_fila(ocorrencias,fila_atendimento, id):
    
    for ocorrencia in ocorrencias:
        if ocorrencia["id"] == id:
            fila_atendimento.append(ocorrencia)
            return True
    return False


# Atender ocorrências da fila
def atender_ocorrencias(fila_atendimento):

    while fila_atendimento:

        ocorrencia = fila_atendimento.pop(0)

        print("Atendendo ocorrência:", ocorrencia["id"])

        if ocorrencia["status"] == "CONCLUIDA":
            print("A ocorrência já está concluída.")
            continue

        status_anterior = ocorrencia["status"]

        novo_status = input(
            "Digite o novo status (ABERTA, EM_ANALISE, CONCLUIDA): "
        )

        resultado = alterar_status(
            [ocorrencia],
            ocorrencia["id"],
            novo_status
        )

        if resultado:
            registrar_historico(
                [ocorrencia],
                ocorrencia["id"],
                novo_status
            )
            print("Status atualizado com sucesso!")

        else:
            print("Não foi possível alterar o status.")
            fila_atendimento.insert(0, ocorrencia)

    print("Fila de atendimento finalizada.")

# Adicionar uma atividade à pilha de histórico.
def adicionar_atividade(pilha_historico, atividade):
    pilha_historico.append(atividade)

#Consultar a última atividade da pilha de histórico.
def consultar_ultima_atividade(pilha_historico):
    if pilha_historico:
        return pilha_historico[-1]
    else:
        return None
#Exibir todas as atividades da pilha de histórico.
def exibir_atividades(pilha_historico):
    if pilha_historico:
        for atividade in reversed(pilha_historico):
            print(atividade)
    else:
        print("Nenhuma atividade registrada.")
        
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
nova = cadastrar_ocorrencia(dados_validos)

print("Total de ocorrências:", len(dados_validos))
print("Nova ocorrência:", nova)