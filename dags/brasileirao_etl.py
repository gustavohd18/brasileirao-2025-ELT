from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import pandas as pd
import os

from etl_utils import extract_matches, save_to_s3

default_args = {
    'owner': 'gustavo',
    'depends_on_past': False,
    'start_date': datetime(2025, 5, 20),
    'retries': 1,
    'retry_delay': timedelta(minutes=2),
}

# This need be changed to the current turn
TURN = 8
BUCKET_NAME = 'brasileirao-2025'
TEMP_CSV_PATH = f'/tmp/rodada_{TURN}.csv'

dag = DAG(
    dag_id='brasileirao_etl',
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
    description='ETL para resultados do Brasileirão e upload para o S3'
)

def extract_transform_task(**kwargs):
    url = f"https://bra.worldfootball.net/tabela_e_jogos/bra-serie-a-2025-spieltag/{TURN}/"
    df = extract_matches(url, TURN)
    df.to_csv(TEMP_CSV_PATH, index=False)
    print(f'Dados salvos em {TEMP_CSV_PATH}')

def load_to_s3_task(**kwargs):
    df = pd.read_csv(TEMP_CSV_PATH)
    save_to_s3(df, BUCKET_NAME, TURN)
    os.remove(TEMP_CSV_PATH)  # clean up temp file

extract_transform = PythonOperator(
    task_id='extract_transform',
    python_callable=extract_transform_task,
    dag=dag
)

load_to_s3 = PythonOperator(
    task_id='load_to_s3',
    python_callable=load_to_s3_task,
    dag=dag
)

extract_transform >> load_to_s3
