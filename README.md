# Orquestração de pipeline com Apache Airflow

## Sumário
1.[Análises Iniciais](#-análises-iniciais)

2.[Tecnologias Utilizadas](#tecnologias-utilizadas)

3.[Passo-a-passo de Execução](#passo-a-passo-de-execução)



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

       - Description: db banvic
       - Host: db
       - Login: data_engineer
       - Password: v3rysecur&pas5w0rd
       - Port: 5432
       - Database: banvic

       <div align="start">
          <img src="img\credenciaisbanvic.png" width="30%"><br>
       </div>

       Após isso clique em *save*

       5.6. De forma análoga, crie a conexão com ID **banvic_dw** e *connection type* igual a **Postgres**
       
       <div align="start">
          <img src="img\dwbanvic1.png" width="45%"><br>
       </div>

      5.7. Nos campos das configurações insira as seguintes credenciais:

       - Description: dw banvic
       - Host: dw_local
       - Login: data_engineer
       - Password: v3rysecur&pas5w0rd
       - Port: 5432
       - Database: dw_banvic

       <div align="start">
          <img src="img\credenciaisbanvicdw.png" width="45%"><br>
       </div>
      
      E por fim, clique em *save*. Dessa forma a **DAG** pode funcionar normalmente. Mas antes disso, será necessário ativar ela.

   6.0.




      


    

