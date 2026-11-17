FIAP - Faculdade de Informática e Administração Paulista

![Logo FIAP](./logo_fiap.png)

# Neighborhood Action Dashboard

**Nome do grupo:** Tribo Nexus

**Nome do projeto:** Neighborhood Action Dashboard

## 👨‍🎓 Integrantes

- Eduarda Queiroz Vila — rm575068 - 1CCOR
- João Lino Santos Braga — rm575103 - 1CCOR
- Daniel da Silva Nogueira — rm575468 - 1CCOS
- Cassiane Maria Andrade Bezerra — rm574274 - 1CCOS

## 👩‍🏫 Professores

**Tutor(a):** Lucas Gomes
**Coordenador(a):** Valter Santiago

## 📜 Descrição

O Neighborhood Action Dashboard é um projeto desenvolvido em Python para simular o registro, a organização e o acompanhamento de problemas relacionados à infraestrutura e à conservação de espaços coletivos de uma comunidade.

A proposta surgiu a partir de uma situação comum em muitos bairros: problemas como iluminação danificada, calçadas sem acessibilidade, acúmulo de lixo e espaços públicos precisando de manutenção nem sempre são organizados de maneira que facilite seu acompanhamento.

Pensando nisso, desenvolvemos uma aplicação que permite cadastrar ocorrências, consultar registros, acompanhar mudanças de situação e gerar indicadores básicos sobre os problemas identificados.

Para representar esse cenário, utilizamos o bairro fictício **Jardim Esperança**. Todas as ocorrências e localidades presentes no projeto são simuladas, sem representar solicitações reais a órgãos públicos.

### Objetivos do projeto

- Atualizar o andamento das ocorrências.
- Manter um histórico simples das alterações.
- Organizar demandas em uma fila de atendimento.
- Registrar problemas identificados na comunidade.
- Organizar ocorrências por categoria e localidade.
- Consultar registros por identificador, categoria e situação.
- Apresentar indicadores que ajudem a compreender os dados cadastrados.

### Categorias utilizadas

| Código | Categoria                        |
| ------ | -------------------------------- |
| ILU    | Iluminação                       |
| ACE    | Acessibilidade                   |
| LIM    | Limpeza                          |
| CON    | Conservação de espaços coletivos |

### Situações das ocorrências

| Status     | Significado                                     |
| ---------- | ----------------------------------------------- |
| ABERTA     | Ocorrência registrada, mas ainda não concluída. |
| EM_ANALISE | Ocorrência em processo de análise.              |
| CONCLUIDA  | Ocorrência marcada como concluída.              |

### Funcionalidades

A aplicação possui um menu interativo no terminal, por meio do qual o usuário pode:

1. Exibir ocorrências cadastradas.
2. Cadastrar uma nova ocorrência.
3. Buscar uma ocorrência por ID.
4. Filtrar ocorrências por categoria.
5. Filtrar ocorrências por status.
6. Alterar o status de uma ocorrência.
7. Consultar um relatório de indicadores.
8. Consultar o histórico de uma ocorrência.
9. Adicionar ocorrências à fila de atendimento.
10. Simular o atendimento das ocorrências da fila.
11. Adicionar atividades à pilha de histórico.
12. Consultar a última atividade registrada.
13. Exibir as atividades armazenadas na pilha.

---

## 📁 Estrutura de pastas

A arquitetura do projeto foi organizada a fim de separar os dados, o código-fonte e a documentação. Assim, facilitando a manutenção e a compreensão dos arquivos.

```text
neighborhood-action-dashboard/
│
├── data/
│   └── ocorrencias.csv
│
├── docs/
│   └── uso_ia.md
│
├── src/
│   └── sistema.py
│
├── README.md
│
└── .gitignore
```

### Descrição dos diretórios e arquivos

**data/**

Armazena o arquivo `ocorrencias.csv`, que contém os registros simulados utilizados na inicialização do sistema.

**docs/**

Reúne a documentação complementar do projeto, incluindo o arquivo `uso_ia.md`, que descreve como a inteligência artificial foi utilizada durante o desenvolvimento.

**src/**

Contém o código-fonte principal da aplicação, localizado no arquivo `sistema.py`.

**README.md**

Este documento, responsável por apresentar o projeto, suas funcionalidades, decisões técnicas e instruções de execução.

**.gitignore**

Define arquivos e diretórios que não devem ser enviados ao repositório Git, como arquivos temporários do Python e ambientes virtuais.

---

## 🧠 Decisões Técnicas

Durante o desenvolvimento, buscamos utilizar estruturas simples que fossem adequadas às necessidades do projeto e aos conteúdos estudados nas três primeiras fases do curso.

### Linguagem e armazenamento

**Python**

Foi escolhido por permitir trabalhar com funções, condicionais, laços de repetição e estruturas de dados de maneira simples e organizada.

**CSV**

Utilizamos um arquivo CSV para armazenar as ocorrências iniciais. Esse formato facilita a leitura dos registros e permite visualizar os dados de maneira organizada.

**Interface textual**

Optamos por uma aplicação executada diretamente no terminal, utilizando um menu numerado para orientar o usuário.

### Estruturas de dados

**Listas**

Utilizadas para armazenar o conjunto de ocorrências e permitir percorrer, consultar e adicionar registros.

**Filas**

Utilizadas para organizar as ocorrências que aguardam atendimento, seguindo o conceito FIFO (_First In, First Out_), em que o primeiro elemento adicionado é o primeiro a ser retirado.

**Pilhas**

Utilizadas para registrar atividades realizadas durante a execução do sistema. Seguem o conceito LIFO (_Last In, First Out_), permitindo consultar a atividade mais recente.

**Dicionários**

Utilizados para criar um índice de ocorrências pelo identificador, facilitando a localização dos registros.

**Hierarquia**

Utilizamos dicionários aninhados para representar a organização:

`Bairro → Categoria → Ocorrências`

Essa estrutura permite agrupar os registros do Jardim Esperança de acordo com suas categorias.

**Matrizes e indicadores**

Foram criadas funções para contabilizar ocorrências por categoria e por situação. A representação combinada utiliza atualmente dicionários aninhados, com ajuste ainda previsto para atender integralmente ao requisito de matriz ou lista de listas.

### Regras lógicas e validações

O sistema utiliza estruturas condicionais para verificar os dados e controlar as operações.

Entre as validações implementadas estão:

- Verificar se o identificador foi informado.
- Verificar se a data de abertura foi informada.
- Impedir a utilização de situações desconhecidas.
- Impedir o cadastro de identificadores já existentes.
- Verificar se descrição e localidade foram preenchidas.
- Verificar se a categoria pertence às opções permitidas.
- Exigir data de conclusão quando uma ocorrência está concluída.
- Impedir que ocorrências não concluídas possuam data de conclusão.

Um exemplo de expressão booleana utilizada é:

```python
if ocorrencia["data_abertura"] is not None and ocorrencia["data_conclusao"] is not None:
```

Nesse caso, o operador `and` exige que as duas datas estejam preenchidas para que o cálculo do tempo de atendimento seja realizado.

Também utilizamos o operador `not` em verificações de ausência de informações e de estruturas vazias. A utilização do operador `or` e a documentação das três condições booleanas distintas exigidas pela atividade ainda precisam ser conferidas na revisão final do código.

### Indicadores

O sistema calcula indicadores básicos para ajudar a compreender os registros.

**Total de ocorrências**

Representa a quantidade total de registros válidos.

**Percentual de ocorrências concluídas**

`(Quantidade de ocorrências concluídas / Total de ocorrências) × 100`

**Percentual de ocorrências pendentes**

`(Quantidade de ocorrências não concluídas / Total de ocorrências) × 100`

**Tempo médio de atendimento**

`Soma dos tempos de atendimento / Quantidade de ocorrências concluídas`

O tempo de atendimento de cada registro é calculado pela diferença entre a data de conclusão e a data de abertura.

Esses indicadores permitem observar a proporção de demandas concluídas, identificar pendências e analisar o tempo médio simulado de atendimento.

---

## 🔧 Como executar o código

Para executar o projeto, é necessário ter o Python instalado no computador.

Não são necessárias bibliotecas externas para a versão atual, pois utilizamos recursos nativos da linguagem.

### 1. Clonar o repositório

```bash
git clone https://github.com/LinoBraga/neighborhood-action-dashboard.git
```

### 2. Acessar a pasta do projeto

```bash
cd neighborhood-action-dashboard
```

### 3. Executar a aplicação

```bash
python src/sistema.py
```

Após a execução, o menu principal será apresentado no terminal, permitindo acessar as funcionalidades disponíveis.

### Arquivo de dados

Os registros iniciais são carregados do seguinte arquivo:

```text
data/ocorrencias.csv
```

**Observação:** as ocorrências cadastradas durante a execução ficam armazenadas na memória do programa. A gravação dessas novas alterações no arquivo CSV não faz parte da implementação atual.

---

## 📎 Links e Observações

### 🔗 Links do Projeto

- [Repositório GitHub](https://github.com/LinoBraga/neighborhood-action-dashboard) — Código-fonte e documentação do projeto.
- [Vídeo de apresentação no YouTube](INSERIR_LINK_DO_VIDEO) — Demonstração do funcionamento da aplicação.

---

## 📢 Observações Gerais

**Participação na Competição:**

[ ] Sim, aceitamos participar.

[ ] Não vamos participar.

**Outras observações:**

O Neighborhood Action Dashboard é um protótipo acadêmico desenvolvido para representar o acompanhamento de demandas comunitárias utilizando dados simulados.

O sistema não possui integração com prefeituras, órgãos públicos ou serviços externos e não garante o atendimento das ocorrências cadastradas.

### Acessibilidade, inclusão e privacidade

Buscamos manter uma aplicação simples de utilizar e compreender, com opções numeradas e mensagens que orientam o usuário durante as operações.

As categorias contemplam diferentes necessidades da comunidade, incluindo iluminação, acessibilidade, limpeza e conservação.

Os registros utilizam dados fictícios e localidades genéricas, sem necessidade de identificação pessoal dos moradores.

### Conclusão e aprendizados

O desenvolvimento deste projeto permitiu aplicar, na prática, conceitos estudados durante as primeiras fases do curso.

Ao longo da construção, trabalhamos com leitura de arquivos CSV, funções, estruturas condicionais, laços de repetição, listas, filas, pilhas, dicionários, validação de dados e cálculos de indicadores.

Além da implementação das funcionalidades, o projeto ajudou a compreender a importância de escolher estruturas adequadas para organizar informações e transformar dados simples em resultados compreensíveis.

Entre as limitações atuais estão a utilização de dados simulados, a interface exclusivamente textual e a ausência de integração com serviços externos.

Mesmo com essas limitações, o projeto demonstra como os fundamentos da programação podem ser aplicados para representar situações cotidianas e organizar informações de uma comunidade.

---

## 📋 Licença

Este projeto foi desenvolvido para fins acadêmicos, como parte da Global Solution 2026.2 da FIAP.

O template utilizado como referência é o FIAP PORTFÓLIO AI, disponibilizado pela FIAP sob a licença Attribution 4.0 International (CC BY 4.0).

Para mais informações: https://creativecommons.org/licenses/by/4.0/
