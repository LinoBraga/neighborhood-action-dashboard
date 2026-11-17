# Neighborhood Action Dashboard

**Global Solution 2026.2**  
**Desafio: CitizenTech**

## Sobre o projeto

O Neighborhood Action Dashboard é um sistema desenvolvido em Python para simular o registro e o acompanhamento de problemas encontrados em uma comunidade.

A ideia surgiu a partir de uma situação bastante comum: problemas como postes com iluminação danificada, calçadas sem acessibilidade, acúmulo de lixo e espaços públicos precisando de manutenção nem sempre são organizados de uma maneira que facilite seu acompanhamento.

Pensando nisso, desenvolvemos uma aplicação que permite registrar essas ocorrências, consultar informações, acompanhar mudanças de status e visualizar alguns indicadores sobre os problemas identificados.

Para o desenvolvimento do projeto, utilizamos o bairro fictício **Jardim Esperança** como cenário. Todas as ocorrências e localidades utilizadas são simuladas.

O objetivo é mostrar como conceitos básicos de programação podem ajudar a organizar informações e facilitar a compreensão das necessidades de uma comunidade.

## O problema que queremos representar

Em uma comunidade, diferentes problemas de infraestrutura podem surgir ao longo do tempo. Sem uma organização adequada, fica difícil saber quais situações foram registradas, quais ainda precisam de atenção e quais já foram concluídas.

Nosso sistema busca representar uma maneira simples de organizar essas informações.

Com ele, é possível manter um conjunto de ocorrências, classificá-las por categoria, consultar seu andamento e gerar um resumo dos dados cadastrados.

É importante destacar que esta é uma aplicação acadêmica. Ela não possui integração com prefeituras ou órgãos públicos e não realiza solicitações reais de serviços.

## O que o sistema permite fazer?

A aplicação possui um menu interativo no terminal. Por meio dele, o usuário consegue:

- Visualizar as ocorrências cadastradas.
- Registrar uma nova ocorrência.
- Pesquisar uma ocorrência pelo seu identificador.
- Filtrar registros por categoria ou situação.
- Alterar o status de uma ocorrência.
- Consultar o histórico de alterações.
- Adicionar ocorrências a uma fila de atendimento.
- Simular o atendimento das ocorrências que estão na fila.
- Registrar e consultar atividades realizadas durante a execução.
- Gerar um relatório com indicadores básicos.

As operações foram organizadas em funções para facilitar a leitura do código e separar as responsabilidades de cada parte do sistema.

## Como as ocorrências são organizadas?

Para facilitar a consulta, definimos quatro categorias, cada uma representada por um código:

| Código | Categoria |
|---|---|
| ILU | Iluminação |
| ACE | Acessibilidade |
| LIM | Limpeza |
| CON | Conservação de espaços coletivos |

Cada ocorrência possui informações que ajudam a identificar e acompanhar o problema:

- **ID:** código único da ocorrência.
- **Categoria:** tipo de problema identificado.
- **Descrição:** explicação breve da situação.
- **Localidade:** rua ou espaço onde o problema foi registrado.
- **Data de abertura:** dia simulado em que a ocorrência foi cadastrada.
- **Status:** situação atual da ocorrência.
- **Data de conclusão:** dia simulado em que a ocorrência foi concluída, quando aplicável.

### Situações das ocorrências

Trabalhamos com três situações:

| Status | Significado |
|---|---|
| ABERTA | A ocorrência foi registrada, mas ainda não foi concluída. |
| EM_ANALISE | A ocorrência está em processo de análise. |
| CONCLUIDA | A ocorrência foi marcada como concluída. |

Os registros iniciais ficam armazenados no arquivo `data/ocorrencias.csv`, que é lido pelo Python durante a inicialização do programa.

Também implementamos validações para identificar registros com informações ausentes ou inconsistentes. Dessa maneira, os dados inválidos podem ser separados dos registros utilizados pelo sistema.

## Estruturas de dados utilizadas

Uma parte importante do projeto foi escolher como armazenar e organizar as informações. Para isso, utilizamos estruturas de dados estudadas durante as primeiras fases do curso.

**Listas**

Utilizamos listas para armazenar as ocorrências carregadas do arquivo CSV. Elas permitem percorrer os registros, realizar pesquisas, adicionar novas ocorrências e calcular indicadores.

**Filas**

A fila de atendimento organiza as ocorrências que aguardam processamento. Utilizamos o conceito FIFO (*First In, First Out*), no qual o primeiro elemento adicionado é o primeiro a ser retirado.

Escolhemos essa estrutura para simular uma ordem de atendimento das demandas cadastradas na fila.

**Pilhas**

A pilha registra atividades realizadas durante a execução do sistema. Ela segue o conceito LIFO (*Last In, First Out*), permitindo consultar a atividade mais recente por meio do último elemento armazenado.

**Dicionários**

Utilizamos dicionários para criar um índice de ocorrências pelo identificador. Assim, em vez de percorrer toda a lista para procurar um ID, podemos acessar o registro diretamente por sua chave.

**Hierarquia**

Também desenvolvemos uma organização hierárquica utilizando dicionários aninhados:

`Bairro → Categoria → Ocorrências`

Essa estrutura representa o bairro Jardim Esperança como nível principal, suas categorias como segundo nível e as ocorrências como elementos agrupados.

**Matrizes e organização dos indicadores**

Criamos funções para contabilizar ocorrências por categoria, por status e pela combinação dessas informações. A função combinada utiliza atualmente dicionários aninhados; sua representação final será ajustada para atender ao formato de matriz ou lista de listas solicitado no desafio.

## Regras e validações

Para evitar que informações incorretas prejudiquem o funcionamento do sistema, implementamos regras de validação durante o cadastro e a análise dos registros.

Entre as verificações realizadas estão:

- O identificador precisa estar preenchido.
- A categoria deve corresponder a uma das opções permitidas.
- A descrição e a localidade não podem estar vazias.
- A data de abertura precisa estar preenchida.
- O status deve ser um dos três valores definidos.
- Uma ocorrência concluída precisa possuir data de conclusão.
- Uma ocorrência que ainda não foi concluída não deve possuir data de conclusão.
- O sistema verifica se o identificador já está cadastrado antes de aceitar uma nova ocorrência.

Também utilizamos estruturas condicionais (`if`, `elif` e `else`) para controlar as operações e decidir qual ação deve ser executada em cada situação.

Um exemplo é a validação utilizada no cálculo do tempo médio de atendimento:

```python
if ocorrencia["data_abertura"] is not None and ocorrencia["data_conclusao"] is not None:
```

Nesse caso, o operador `and` exige que as duas datas estejam preenchidas. Somente assim o sistema realiza a subtração entre a data de abertura e a data de conclusão.

Outras condições utilizam os operadores `not` para verificar situações em que uma informação está ausente ou uma estrutura não possui elementos.

## Indicadores do sistema

Além de organizar as ocorrências, o sistema calcula alguns indicadores para apresentar uma visão geral dos registros.

Atualmente, trabalhamos com os seguintes cálculos:

**Total de ocorrências**

Representa a quantidade de registros válidos carregados pelo sistema.

**Percentual de ocorrências concluídas**

Mostra qual parte das ocorrências já foi concluída em relação ao total.

Fórmula:

`(Quantidade de ocorrências concluídas / Total de ocorrências) × 100`

**Percentual de ocorrências pendentes**

Indica a proporção de ocorrências que ainda não foram concluídas.

Fórmula:

`(Quantidade de ocorrências não concluídas / Total de ocorrências) × 100`

**Tempo médio de atendimento**

Calcula quantos dias simulados, em média, foram necessários para concluir as ocorrências finalizadas.

Fórmula:

`Soma dos tempos de atendimento / Quantidade de ocorrências concluídas`

O tempo de atendimento de cada ocorrência é calculado pela diferença entre a data de conclusão e a data de abertura.

Esses indicadores permitem observar a quantidade de demandas concluídas, identificar pendências e compreender o tempo médio simulado de atendimento.

As funções de contagem por categoria e situação também ajudam a identificar quais tipos de problemas aparecem com maior frequência no conjunto de dados.

## Como executar o projeto?

Para executar o sistema, é necessário ter o Python instalado.

Primeiro, clone o repositório:

```bash
git clone https://github.com/LinoBraga/neighborhood-action-dashboard.git
```

Entre na pasta do projeto:

```bash
cd neighborhood-action-dashboard
```

Depois, execute o arquivo principal:

```bash
python src/sistema.py
```

O menu será apresentado diretamente no terminal, permitindo acessar as funcionalidades disponíveis.

O arquivo com os registros iniciais está localizado em:

```text
data/ocorrencias.csv
```

**Observação:** as novas ocorrências cadastradas durante a execução são mantidas na memória do programa. A gravação dessas alterações de volta no CSV não faz parte da implementação atual.

## Acessibilidade, inclusão e privacidade

Durante o desenvolvimento, buscamos manter uma aplicação simples de utilizar e compreender.

A interface utiliza um menu com opções numeradas e mensagens que orientam o usuário durante as operações.

Também consideramos importante representar diferentes necessidades da comunidade. Por isso, incluímos categorias relacionadas à iluminação, acessibilidade, limpeza e conservação dos espaços coletivos.

Em relação à privacidade, utilizamos dados fictícios e localidades genéricas. O sistema não exige nomes, documentos, contatos ou outras informações pessoais dos moradores.

## Conclusão e aprendizados

O desenvolvimento do Neighborhood Action Dashboard foi uma oportunidade de aplicar, em um projeto prático, conceitos de programação que estudamos durante as primeiras fases do curso.

Ao longo da construção, trabalhamos com leitura de arquivos CSV, criação de funções, estruturas condicionais, laços de repetição, listas, filas, pilhas, dicionários e cálculos de indicadores.

Mais do que desenvolver um programa que executa determinadas operações, o projeto nos permitiu entender a importância de escolher estruturas adequadas para organizar informações e transformar dados simples em resultados que possam ser compreendidos.

Sabemos que a aplicação possui limitações, principalmente por utilizar dados simulados, funcionar apenas pelo terminal e não possuir integração com serviços externos. Mesmo assim, ela demonstra como os fundamentos da programação podem ser utilizados para representar problemas cotidianos e organizar informações de maneira estruturada.

## Equipe

**Integrantes:**

- [João Lino Santos Braga] — RM [rm575103]
- [Daniel da Silva Nogueira] — RM [rm575468]
- [Eduarda Queiroz] — RM [rm575068]
- [Cassiane Andrade] — RM [rm574274]

## Vídeo de apresentação

[Falta só o vídeo: inserir aqui.]

---

**FIAP — Global Solution 2026.2**  
**CitizenTech | Neighborhood Action Dashboard**