import pandas as pd
from airflow.decorators import dag, task
from airflow.providers.postgres.hooks.postgres import PostgresHook
from pendulum import datetime
from pathlib import Path


AIRFLOW_HOME = Path('/opt/airflow')
RAW_DATA_PATH = AIRFLOW_HOME / 'raw_data'
PROCESSED_DATA_PATH = AIRFLOW_HOME / 'processed_data'
TABLES_BANVIC = ["agencias", "clientes",
                 "colaboradores", "contas",
                 "propostas_credito"]


@dag(
    dag_id='processamento_dados_banvic',
    start_date=datetime(2025, 9, 1),
    schedule=None,
    catchup=False,
    tags=['pandas', 'sql', 'etl'],
    doc_md="""
    ### DAG de Processamento de Dados da Banvic

    Esta DAG realiza a extração e transformação de dados a partir de arquivos csv e de um banco de dados.
    """
)
def processamento_dados_pipeline():
    @task(task_id="verifica_pastas_destino")
    def garantir_pastas_de_destino():
        (PROCESSED_DATA_PATH / 'csv').mkdir(parents=True, exist_ok=True)
        (PROCESSED_DATA_PATH / 'sql').mkdir(parents=True, exist_ok=True)

    @task(task_id="processar_csv_transacoes")
    def processar_csv_transacoes():
        arquivo_origem = RAW_DATA_PATH / 'transacoes.csv'
        arquivo_destino = PROCESSED_DATA_PATH / 'csv' / 'transacoes_processado.csv'

        print(f"Lendo de: {arquivo_origem}")
        df = pd.read_csv(arquivo_origem)
        print(f"Salvando {len(df)} linhas em: {arquivo_destino}")
        df.to_csv(arquivo_destino, index=False)
        return str(arquivo_destino)

    @task(task_id="processar_tabela_banvic")
    def processar_tabela_banvic():
        hook = PostgresHook(postgres_conn_id='banvic_source_db')
        for tabela in TABLES_BANVIC:
            sql_query = f"select * from {tabela};"
            df = hook.get_pandas_df(sql=sql_query)
            arquivo_destino = PROCESSED_DATA_PATH / 'sql'
            df.to_csv(arquivo_destino / f"{tabela}.csv", index=False)
        
        return str(arquivo_destino)

    pastas_garantidas = garantir_pastas_de_destino()

    pastas_garantidas >> [
        processar_csv_transacoes(), processar_tabela_banvic()]


processamento_dados_pipeline()
