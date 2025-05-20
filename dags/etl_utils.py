import requests
from bs4 import BeautifulSoup
import pandas as pd
from io import StringIO
import boto3
from airflow.providers.amazon.aws.hooks.s3 import S3Hook


def extract_matches(url, turn):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find_all('table')[1]
    rows = table.find_all('tr')

    data = []
    last_date = None

    for row in rows:
        cols = row.find_all('td')
        if len(cols) < 6:
            continue

        raw_date = cols[0].text.strip()
        if raw_date and any(char.isdigit() for char in raw_date) and '.' in raw_date:
            last_date = raw_date
        if last_date is None:
            continue

        home = cols[2].text.strip()
        away = cols[4].text.strip()
        result = cols[5].text.strip()
        if ':' not in result:
            continue

        clean_result = result.split('(')[0].strip()
        try:
            home_score, away_score = map(int, clean_result.split(':'))
        except ValueError:
            continue

        goal_difference = home_score - away_score
        total_goals = home_score + away_score

        winner = home if home_score > away_score else away if away_score > home_score else "Draw"

        data.append({
            'date': last_date,
            'home_team': home,
            'away_team': away,
            'home_score': home_score,
            'away_score': away_score,
            'goal_difference': goal_difference,
            'total_goals': total_goals,
            'winner': winner,
            'turn': turn
        })

    return pd.DataFrame(data)

# def save_to_s3_(df, bucket_name, turn):
#     s3_key = f'rodadas/semana-{turn}/rodada_{turn}.csv'
#     csv_buffer = StringIO()
#     df.to_csv(csv_buffer, index=False)

#     s3 = boto3.client('s3')
#     s3.put_object(Bucket=bucket_name, Key=s3_key, Body=csv_buffer.getvalue())

#     print(f'Enviado para s3://{bucket_name}/{s3_key}')

def save_to_s3(df, bucket_name, turn, aws_conn_id='aws_default'):
    s3_key = f'rodadas/semana-{turn}/rodada_{turn}.csv'
    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=False)
    csv_buffer.seek(0)  # importante resetar o cursor

    hook = S3Hook(aws_conn_id=aws_conn_id)
    hook.load_string(
        string_data=csv_buffer.getvalue(),
        key=s3_key,
        bucket_name=bucket_name,
        replace=True
    )
    print(f'Enviado para s3://{bucket_name}/{s3_key}')