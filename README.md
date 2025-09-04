# 🚀 Orquestração de Pipeline com Apache Airflow

![Airflow](https://img.shields.io/badge/Airflow-017CEE?style=for-the-badge&logo=Apache%20Airflow&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Postgres](https://img.shields.io/badge/Postgres-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)

## 📑 Sumário  
1. [Análises Iniciais](#-análises-iniciais)  
2. [Tecnologias Utilizadas](#-tecnologias-utilizadas)  
3. [Pré-requisitos](#-pré-requisitos)  
4. [Estrutura do Projeto](#-estrutura-do-projeto)  
5. [Lógica do Fluxo de Dados](#-lógica-do-fluxo-de-dados)  
6. [Processos da DAG](#-processos-da-dag)  
7. [Passo-a-passo de Execução](#passo-a-passo-de-execução)  



------------------------------------------------------------------------

# 📊 Análises Iniciais

Este projeto é um desafio prático do processo seletivo para o programa
**Indicium Lighthouse**.

🎯 **Objetivo:** Estabelecer um fluxo de extração de dados de um banco
fictício **Banvic** (arquivos CSV e SQL) e carregar os dados em um banco
**PostgreSQL**, orquestrado pelo **Apache Airflow**.

------------------------------------------------------------------------

# 🛠 Tecnologias Utilizadas

-   🌀 **Apache Airflow 3.0.6**\
-   🐍 **Python/Pandas**\
-   🐳 **Docker & Docker Compose**

------------------------------------------------------------------------

# ⚙ Pré-requisitos

Antes de rodar o projeto, é necessário ter:

-   📦 **Docker**
-   📦 **Docker Compose**
-   🌐 **Acesso à internet**
-   🖥️ **Git** (se optar por clonar o repositório)
-   🛠 **DBeaver** *(opcional, apenas para visualizar o banco)*

------------------------------------------------------------------------

# 🗂 Estrutura do Projeto
```
desafio-LH-ED/
│
├── dags/
│   ├── processamento_dados_banvic.py
|   └── ...
│
├── raw_data/
│   ├── transacoes.csv
│   └── banvic.sql
│
├── processed_data/
│   └── [data de execução]/
│                 ├── csv/
│                 └── sql/
├── config/
│   └── ...
├── dbdata/    
│   └── ...
├── logs/
│   └── ...
├── plugins/
│   └── ...
├── img/
│   └── ...
│
├── docker-compose.yaml
├── .env
├── .gitignore
├── README.md
├── LICENSE



```

------------------------------------------------------------------------

# 🔄 Lógica do Fluxo de Dados

O fluxo é realizado através do pipeline orquestrado pelo Apache Airflow. 

O processo ocorre 4:35 da manhã todos os dias através da DAG ````processamento_dados_banvic````.

Os dados saem da fonte que são um arquivo CSV bruto e um banco de dados PostgreSQL disponíveis no diretorio *raw_data*. 

Toda 4:35 da manhã o pipeline extrai os dados e cria um diretório novo dentro de *processed_data* contendo o dia em que a DAG rodou e divindo entre *csv* para os arquivos extraídos e *sql* para as tabelas retiradas   dobanco de dados e transformados em CSV. As pastas  do data lake ficam no seguinte formato:
```
[ano-mês-dia] / [fonte de dados] /[nome tabela ou csv].csv
```
------------------------------------------------------------------------

# 📂 Processos da DAG

A DAG é composta pelas seguintes *tasks*
<table>
  <tr>
    <th>Task</th>
    <th>Descrição</th>
  </tr>
  <tr>
    <td>🗂 <b>define_pastas_destino</b></td>
    <td>Cria os diretórios de saída para os dados processados</td>
  </tr>
  <tr>
    <td>📑 <b>processar_csv_transacoes</b></td>
    <td>Processa e organiza os arquivos CSV brutos</td>
  </tr>
  <tr>
    <td>🗄 <b>processar_tabelas_banvic</b></td>
    <td>Extrai tabelas do banco Banvic e converte para CSV</td>
  </tr>
  <tr>
    <td>⬆ <b>carregar_csv_dw_banvic</b></td>
    <td>Carrega dados CSV no Data Warehouse</td>
  </tr>
  <tr>
    <td>⬆ <b>carregar_sql_dw_banvic</b></td>
    <td>Carrega dados SQL no Data Warehouse</td>
  </tr>
</table>


# ▶ Passo-a-passo de Execução

# Passo-a-passo de execução

 1. Para executar o projeto é necessário realizar o **download** do repositório ou    clonar com o seguinte comando no diretório desejado:

    ```sh
    git clone https://github.com/leonardo-vargas-de-paula/desafio-LH-ED.git
    ```
    Em seguida entre no diretório correspondente ao **root** do projeto *desafio-LH-ED*

 2. Inicialize o Apache Airflow na sua primeira execução:

    ```
    docker-compose up airflow-init
    ```
 3. Inicializar os serviços:
    ```sh
    docker-compose up -d
    ```
    OBS: É importante utilizar o comando **-d** para evitar possíveis travamentos no terminal.

 4. Entre no webserver do Airflow na URL  ``http://localhost:8080`` com login ``airflow`` e senha ``airflow``


5.  Configure as conexões referentes ao banco de dados do Banvic e o Datawarehouse de destino dentro do webserver:
    
       5.1. Localize o botão de configurações de admin:
        
       <div align="start">
          <img src="img\config.png" width="10%"><br>
       </div>
    
       5.2.Selecione a opção *Connections*

       <div align="start">
          <img src="img\connections.png" width="10%"><br>
       </div>
       
       5.3.Clique em *Add Connection*
       
       <div align="start">
          <img src="img\addconnection.png" width="20%"><br>
       
       </div>

       5.4. No campo *Connection ID* escreva **banvic_source_db** para identificar o ID do banco de dados do Banvic e *connection type* igual a **Postgres**.
                                          
       <div align="start">
          <img src="img\dbbanvic1.png" width="30%"><br>
       </div>
    
       5.5. Nos campos das configurações insira as seguintes credenciais:

      <table> 
      <tr> <th>Campo</th> <th>Valor</th> </tr> 
      <tr> <td>Description</td> <td>db banvic</td> </tr> 
      <tr> <td>Host</td> <td>db</td> </tr> 
      <tr> <td>Login</td> <td>data_engineer</td> </tr> 
      <tr> <td>Password</td> <td>v3rysecur&pas5w0rd</td> </tr> 
      <tr> <td>Port</td> <td>5432</td> </tr> <tr> <td>Database</td> 
      <td>banvic</td> </tr> 
      </table>   

       <div align="start">
          <img src="img\credenciaisbanvic.png" width="30%"><br>
       </div>

       Após isso clique em *save*

       5.6. De forma análoga, crie a conexão com ID **banvic_dw** e *connection type* igual a **Postgres**
       
       <div align="start">
          <img src="img\dwbanvic1.png" width="45%"><br>
       </div>

      5.7. Nos campos das configurações insira as seguintes credenciais:

       <table> <tr> <th>Campo</th> <th>Valor</th> </tr> 
       <tr> <td>Description</td> 
       <td>dw banvic</td> </tr> <tr> <td>Host</td> <td>dw_local</td> 
       </tr> <tr> <td>Login</td> <td>data_engineer</td> </tr> 
       <tr> <td>Password</td> <td>v3rysecur&pas5w0rd</td> </tr> 
       <tr> <td>Port</td> <td>5432</td> </tr> 
       <tr> <td>Database</td> <td>dw_banvic</td> </tr> 
       </table>

       <div align="start">
          <img src="img\credenciaisbanvicdw.png" width="45%"><br>
       </div>
      
      E por fim, clique em *save*. Dessa forma a **DAG** pode funcionar normalmente. Mas antes disso, será necessário ativá-la.

   6. No menu lateral, clique no botão *DAGS*:

      <div align="start">
      <img src="img\botaodags.png" width="20%"><br>
      </div>

      6.1.Realize uma busca pela DAG chamada    
      ````processamento_dados_banvic````

   7. Ao encontrar a DAG desejada, clique nela para ter um overview e verificar suas características.

   [adicionar imagem overview]

   8. Clique no switch para ativar a DAG

   [adicionar imagem switch]

   9.  Pronto! A DAG esta agendada para rodar as 4:35 da manhã. Caso deseje rodar manualmente, clique em *trigger*.

   [adicionar imagem botão trigger]
