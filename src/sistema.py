import csv

pilha_historico = []  # pilha
fila_atendimento = []  # fila de atendimento


# Carregar os dados do arquivo CSV
def carregar_ocorrencias(caminho_arquivo):
    ocorrencias = []
    with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
        leitor = csv.DictReader(arquivo)
        for linha in leitor:

            # Data abertura e data de conclusão devem ser convertidas para inteiro, caso contrário, devem ser None.
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


# Verificar se a ocorrência é válida
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


# Separar e tratar dados
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


# Criando indice de ocorrências para busca rápida
def criar_indice_ocorrencias(ocorrencias):
    indice = {}
    for ocorrencia in ocorrencias:
        id = ocorrencia["id"]
        indice[id] = ocorrencia
    return indice


# Busca de ocorrências por ID, categoria e status.
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


# Cadastrando ocorrências
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

    # Status inicial da ocorrência é sempre "ABERTA" e data de conclusão é None
    status = "ABERTA"
    data_conclusao = None

    ocorrencia = {
        "id": id_ocorrencia,
        "categoria": categoria,
        "descricao": descricao,
        "localidade": localidade,
        "data_abertura": int(data_abertura) if data_abertura else None,
        "status": status,
        "data_conclusao": int(data_conclusao) if data_conclusao else None,
    }

    erros = validar_ocorrencia(ocorrencia)
    if erros:
        print("Ocorrência inválida:", erros)
        return None
    else:
        # Adicionando a ocorrência à lista de ocorrências
        ocorrencias.append(ocorrencia)
        return ocorrencia


# Alterando status de ocorrências
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
                ocorrencia["data_conclusao"] = int(
                    input("Digite a data de conclusão da ocorrência: ")
                )
            return True
    return False


# Registrar histórico de alterações de status
def registrar_historico(ocorrencias, id, novo_status):
    for ocorrencia in ocorrencias:
        if ocorrencia["id"] == id:
            if "historico" not in ocorrencia:
                ocorrencia["historico"] = []
            ocorrencia["historico"].append(
                {
                    "status": novo_status,
                    "data": int(input("Digite a data da alteração de status: ")),
                }
            )
            return True
    return False


# Listar histórico de alterações de status
def listar_historico(ocorrencias, id):
    for ocorrencia in ocorrencias:
        if ocorrencia["id"] == id:
            if "historico" in ocorrencia:
                return ocorrencia["historico"]
            else:
                return []
    return None


# Adicionar fila de ocorrências. Retorna True se conseguir adicionar e False se não encontrar.
def adicionar_fila(ocorrencias, fila_atendimento, id):
    for ocorrencia in ocorrencias:
        if ocorrencia["id"] == id:
            fila_atendimento.append(ocorrencia)
            return True
    return False



# Atender ocorrências da fila
def atender_ocorrencias(fila_atendimento):
    quantidade_inicial = len(fila_atendimento)

    if quantidade_inicial == 0:
        print("Não existem ocorrências na fila de atendimento.")
        return

    for _ in range(quantidade_inicial):
        ocorrencia = fila_atendimento.pop(0)

        print("\nAtendendo ocorrência:", ocorrencia["id"])

        if ocorrencia["status"] == "CONCLUIDA":
            print("A ocorrência já está concluída.")
            continue

        status_anterior = ocorrencia["status"]

        novo_status = input(
            "Digite o novo status (ABERTA, EM_ANALISE, CONCLUIDA): "
        ).strip().upper()

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

            adicionar_atividade(
                pilha_historico,
                f"Ocorrência {ocorrencia['id']}: "
                f"{status_anterior} -> {novo_status}"
            )

            print("Status atualizado com sucesso!")

        else:
            print("Não foi possível alterar o status.")
            print("Ocorrência devolvida ao final da fila.")

            fila_atendimento.append(ocorrencia)

    print("\nAtendimento da fila finalizado.")

    if fila_atendimento:
        print("Ocorrências aguardando atendimento:", len(fila_atendimento))
    else:
        print("Todas as ocorrências da fila foram processadas.")



# Adicionar uma atividade à pilha de histórico
def adicionar_atividade(pilha_historico, atividade):
    pilha_historico.append(atividade)


# Consultar a última atividade da pilha de histórico
def consultar_ultima_atividade(pilha_historico):
    if pilha_historico:
        return pilha_historico[-1]
    else:
        return None


# Exibir todas as atividades da pilha de histórico
def exibir_atividades(pilha_historico):
    if pilha_historico:
        for atividade in reversed(pilha_historico):
            print(atividade)
    else:
        print("Nenhuma atividade registrada.")


# Recebe uma lista de ocorrências e coloca cada ocorrência dentro da categoria correspondente sendo bairro a hierarquia principal
def organizar_ocorrencias_por_categoria(ocorrencias):
    organizadas = {}
    for ocorrencia in ocorrencias:
        categoria = ocorrencia["categoria"]
        if categoria not in organizadas:
            organizadas[categoria] = []
        organizadas[categoria].append(ocorrencia)
    return organizadas


def organizar_ocorrencias_por_bairro(ocorrencias):
    organizadas = {}
    for ocorrencia in ocorrencias:
        bairro = ocorrencia["localidade"]
        if bairro not in organizadas:
            organizadas[bairro] = []
        organizadas[bairro].append(ocorrencia)
    return organizadas


# Organizar hierarquia
def organizar_hierarquia(ocorrencias):
    organizadas = {"Jardim Esperanca": {}}

    for ocorrencia in ocorrencias:
        bairro = "Jardim Esperanca"
        categoria = ocorrencia["categoria"]
        if categoria not in organizadas[bairro]:
            organizadas[bairro][categoria] = []
        organizadas[bairro][categoria].append(ocorrencia)
    return organizadas


# Matriz que conta as ocorrências por categoria
def gerar_matriz_categorias(ocorrencias):
    matriz = {}
    for ocorrencia in ocorrencias:
        categoria = ocorrencia["categoria"]
        if categoria not in matriz:
            matriz[categoria] = 0
        matriz[categoria] += 1
    return matriz


# Gerar matriz que conta as ocorrências por status
def gerar_matriz_status(ocorrencias):
    matriz = {}
    for ocorrencia in ocorrencias:
        status = ocorrencia["status"]
        if status not in matriz:
            matriz[status] = 0
        matriz[status] += 1
    return matriz


# Gerando a matriz de status e categorias das ocorrências
def gerar_matriz_status_e_categorias(ocorrencias):
    matriz = {}
    for ocorrencia in ocorrencias:
        categoria = ocorrencia["categoria"]
        status = ocorrencia["status"]
        if categoria not in matriz:
            matriz[categoria] = {}
        if status not in matriz[categoria]:
            matriz[categoria][status] = 0
        matriz[categoria][status] += 1
    return matriz


# Calcular o percentual de ocorrências concluídas em relação ao total de ocorrências
def calcular_percentual_concluidas(ocorrencias):
    total = len(ocorrencias)

    if total == 0:
        return 0.0
    concluidas = 0
    for ocorrencia in ocorrencias:
        if ocorrencia["status"] == "CONCLUIDA":
            concluidas = concluidas + 1
    percentual = (concluidas / total) * 100
    return percentual


# Calcula o percentual pendente de ocorrências em relação ao total de ocorrências
def calcular_percentual_pendentes(ocorrencias):
    total = len(ocorrencias)
    if total == 0:
        return 0.0
    pendentes = 0
    for ocorrencia in ocorrencias:
        if ocorrencia["status"] != "CONCLUIDA":
            pendentes = pendentes + 1
    percentual = (pendentes / total) * 100
    return percentual


# Calcula o tempo médio de atendimento das ocorrências concluídas
def calcular_tempo_medio_atendimento(ocorrencias):
    total = 0
    count = 0
    for ocorrencia in ocorrencias:
        if ocorrencia["status"] == "CONCLUIDA":
            if (
                ocorrencia["data_abertura"] is not None
                and ocorrencia["data_conclusao"] is not None
            ):
                tempo_atendimento = (
                    ocorrencia["data_conclusao"] - ocorrencia["data_abertura"]
                )
                total += tempo_atendimento
                count += 1
    if count == 0:
        return 0.0
    tempo_medio = total / count
    return tempo_medio


# Relatório
def gerar_relatorio(ocorrencias):
    total_ocorrencias = len(ocorrencias)
    percentual_concluidas = calcular_percentual_concluidas(ocorrencias)
    percentual_pendentes = calcular_percentual_pendentes(ocorrencias)
    tempo_medio_atendimento = calcular_tempo_medio_atendimento(ocorrencias)

    relatorio = {
        "total_ocorrencias": total_ocorrencias,
        "percentual_concluidas": percentual_concluidas,
        "percentual_pendentes": percentual_pendentes,
        "tempo_medio_atendimento": tempo_medio_atendimento,
    }

    return relatorio


# Exibir ocorrências
def exibir_ocorrencias(ocorrencias):
    if not ocorrencias:
        print("Nenhuma ocorrência encontrada.")
        return

    for ocorrencia in ocorrencias:
        print("ID:", ocorrencia["id"])
        print("Status:", ocorrencia["status"])
        print("Categoria:", ocorrencia["categoria"])
        print("Descrição:", ocorrencia["descricao"])
        print("Localidade:", ocorrencia["localidade"])
        print("Data de Abertura:", ocorrencia["data_abertura"])
        print("Data de Conclusão:", ocorrencia["data_conclusao"])
        print("-" * 40)


# Exibir o menu ao usuário
def exibir_menu():
    print("==============================================")
    print("       NEIGHBORHOOD ACTION DASHBOARD")
    print("==============================================")
    print("1. Exibir ocorrências")
    print("2. Cadastrar ocorrência")
    print("3. Buscar ocorrência por ID")
    print("4. Buscar por categoria")
    print("5. Buscar por status")
    print("6. Alterar status")
    print("7. Exibir relatório")
    print("8. Exibir histórico")
    print("9. Adicionar ocorrência à fila de atendimento")
    print("10. Atender ocorrências da fila")
    print("11. Adicionar atividade à pilha de histórico")
    print("12. Consultar última atividade da pilha de histórico")
    print("13. Exibir atividades da pilha de histórico")
    print("0. Sair")


# Função principal do sistema
def main():
    todas_ocorrencias = carregar_ocorrencias("data/ocorrencias.csv")
    ocorrencias, dados_invalidos = separar_ocorrencias(todas_ocorrencias)
    indice = criar_indice_ocorrencias(ocorrencias)

    while True:
        exibir_menu()
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            exibir_ocorrencias(ocorrencias)
        elif opcao == "2":
            nova_ocorrencia = cadastrar_ocorrencia(ocorrencias)
            if nova_ocorrencia:
                indice[nova_ocorrencia["id"]] = nova_ocorrencia
                adicionar_atividade(
                    pilha_historico,
                    f"Nova ocorrência cadastrada: {nova_ocorrencia['id']}",
                )
        elif opcao == "3":
            id = input("Digite o ID da ocorrência: ")
            ocorrencia = buscar_por_id(indice, id)
            if ocorrencia:
                exibir_ocorrencias([ocorrencia])
            else:
                print("Ocorrência não encontrada.")
        elif opcao == "4":
            categoria = input("Digite a categoria (ILU, ACE, LIM, CON): ")
            resultados = buscar_por_categoria(ocorrencias, categoria)
            exibir_ocorrencias(resultados)
        elif opcao == "5":
            status = input("Digite o status (ABERTA, EM_ANALISE, CONCLUIDA): ")
            resultados = buscar_por_status(ocorrencias, status)
            exibir_ocorrencias(resultados)
        elif opcao == "6":
            id = input("Digite o ID da ocorrência: ")
            novo_status = input(
                "Digite o novo status (ABERTA, EM_ANALISE, CONCLUIDA): "
            )
            resultado = alterar_status(ocorrencias, id, novo_status)
            if resultado:
                adicionar_atividade(
                    pilha_historico,
                    f"Status da ocorrência {id} atualizado para {novo_status}",
                )
                registrar_historico(ocorrencias, id, novo_status)
                print("Status atualizado com sucesso!")
            else:
                print("Não foi possível alterar o status.")
        elif opcao == "7":
            relatorio = gerar_relatorio(ocorrencias)
            print(relatorio)
        elif opcao == "8":
            id = input("Digite o ID da ocorrência: ")
            historico = listar_historico(ocorrencias, id)
            if historico is not None:
                for registro in historico:
                    print(registro)
            else:
                print("Ocorrência não encontrada.")
        elif opcao == "9":
            id = input("Digite o ID da ocorrência: ")
            resultado = adicionar_fila(ocorrencias, fila_atendimento, id)
            if resultado:
                adicionar_atividade(
                    pilha_historico,
                    f"Ocorrência {id} adicionada à fila de atendimento.",
                )
                print("Ocorrência adicionada à fila de atendimento.")
            else:
                print("Ocorrência não encontrada.")
        elif opcao == "10":
            atender_ocorrencias(fila_atendimento)
        elif opcao == "11":
            atividade = input(
                "Digite a atividade a ser adicionada à pilha de histórico: "
            )
            adicionar_atividade(pilha_historico, atividade)
            print("Atividade adicionada à pilha de histórico.")
        elif opcao == "12":
            ultima_atividade = consultar_ultima_atividade(pilha_historico)
            if ultima_atividade:
                print("Última atividade:", ultima_atividade)
            else:
                print("Nenhuma atividade registrada.")
        elif opcao == "13":
            exibir_atividades(pilha_historico)
        elif opcao == "0":
            print("Saindo do sistema...")
            break
        else:
            print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    main()
