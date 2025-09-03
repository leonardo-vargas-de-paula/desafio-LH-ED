# Orquestração de pipeline com Apache Airflow

## Sumário
1.[Análises Iniciais](#-análises-iniciais)

2.[Tecnologias Utilizadas](#tecnologias-utilizadas)



[terminar depois]

# 📊 Análises Iniciais

Este projeto é um desafio prático do processo seletivo para o programa **Indicium Lighthouse**

O objetivo é estabelecer um fluxo de extração de dados de um banco fiticio "Banvic" no formato CSV e SQL e carregar os dados em um banco PostgreSQL.

# Tecnologias Utilizadas

- **Apache Airflow 3.0.6**
- **Python/Pandas**
- **Docker**

# Pré-requisitos

Para o funcionamento adequado é necessário ter instalado:

- **Docker**
- **Docker Compose**
- **\*Git (caso clone o repositório)**

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


5. Configure as conexões referentes ao banco de dados do Banvic e o Datawarehouse de destino dentro do webserver:

    5.1.

    5.2.

    5.3.

    5.4.

    5.5.
    

