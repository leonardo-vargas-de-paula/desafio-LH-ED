import pandas as pd
from airflow.decorators import dag, task
from airflow.providers.postgres.hooks.postgres import PostgresHook
from pendulum import datetime
from pathlib import Path
import os

AIRFLOW_HOME = Path('/opt/airflow')
RAW_DATA_PATH = AIRFLOW_HOME / 'raw_data'
PROCESSED_DATA_PATH = AIRFLOW_HOME / 'processed_data'

TABLES_BANVIC = ["agencias", "clientes",
                 "colaboradores", "contas",
                 "propostas_credito"]

@dag(
    dag_id='processamento_dados_banvic',
    start_date=datetime(2025, 9, 1),
    schedule="35 4 * * *",
    catchup=False,
    tags=['pandas', 'sql', 'etl'],
    doc_md="""
   ### DAG de Processamento de Dados da Banvic

    Esta DAG realiza a extração e transformação de dados a partir de arquivos csv e de um banco de dados.
    """
)
def processamento_dados_pipeline():

    @task(task_id="define_pastas_destino")
    def definir_pastas_de_destino(**kwargs):
        execution_date_str = kwargs['ds']

        base_path_for_date = PROCESSED_DATA_PATH / execution_date_str
        csv_path = base_path_for_date / 'csv'
        sql_path = base_path_for_date / 'sql'

        csv_path.mkdir(parents=True, exist_ok=True)
        sql_path.mkdir(parents=True, exist_ok=True)

        return {'csv_path': str(csv_path), 'sql_path': str(sql_path)}

    @task(task_id="processar_csv_transacoes")
    def processar_csv_transacoes(path: dict):

        arquivo_origem = RAW_DATA_PATH / 'transacoes.csv'

        csv_path = Path(path['csv_path'])
        arquivo_destino = csv_path / 'transacoes.csv'

        df = pd.read_csv(arquivo_origem)

        df.to_csv(arquivo_destino, index=False)

    @task(task_id="processar_tabelas_banvic")
    def processar_tabelas_banvic(path: dict):

        hook = PostgresHook(postgres_conn_id='banvic_source_db')

        sql_path = Path(path['sql_path'])

        for tabela in TABLES_BANVIC:
            sql_query = f"SELECT * FROM {tabela};"
            df = hook.get_pandas_df(sql=sql_query)

            arquivo_destino = sql_path / f"{tabela}.csv"
            df.to_csv(arquivo_destino, index=False)

    @task(task_id="carregar_csv_dw_banvic")
    def carregar_csv_dw_banvic(path: dict):
        hook_dw = PostgresHook(postgres_conn_id='banvic_dw')
        engine_dw = hook_dw.get_sqlalchemy_engine()
        csv_path = Path(path['csv_path'])

        with engine_dw.connect() as connection:
            for arquivo in os.listdir(csv_path):
                caminho_do_arquivo = os.path.join(csv_path, arquivo)
                nome = str(arquivo).replace('.csv', '')
                df = pd.read_csv(caminho_do_arquivo)
                df.to_sql(
                    nome,
                    connection,
                    if_exists='replace',
                    index=False
                )
    @task(task_id="carregar_sql_dw_banvic")
    def carregar_sql_dw_banvic(path: dict):
        hook_dw = PostgresHook(postgres_conn_id='banvic_dw')
        engine_dw = hook_dw.get_sqlalchemy_engine()
        sql_path = Path(path['sql_path'])

        with engine_dw.connect() as connection:
            for arquivo in os.listdir(sql_path):
                caminho_do_arquivo = os.path.join(sql_path, arquivo)
                nome = str(arquivo).replace('.csv', '')
                df = pd.read_csv(caminho_do_arquivo)
                df.to_sql(
                    nome,
                    connection,
                    if_exists='replace',
                    index=False
                )

    pastas_destino = definir_pastas_de_destino()

    processar_csv_transacoes = processar_csv_transacoes(path=pastas_destino)
    processar_tabelas_banvic = processar_tabelas_banvic(path=pastas_destino)
    carregar_csv_dw_banvic = carregar_csv_dw_banvic(path=pastas_destino)
    carregar_sql_dw_banvic = carregar_sql_dw_banvic(path=pastas_destino)





    [processar_csv_transacoes, processar_tabelas_banvic] >> carregar_csv_dw_banvic >> carregar_sql_dw_banvic

processamento_dados_pipeline()
