from airflow import DAG
from airflow.decorators import task
from datetime import datetime
from confluent_kafka import Consumer
import json, os, csv

default_args = {
    'start_date': datetime(2025, 6, 30),
}

with DAG(
    dag_id="etl_crypto_prices",
    schedule="*/2 * * * *",
    catchup=False,
    default_args=default_args,
    tags=["kafka", "etl"]
) as dag:

    @task()
    def extract():
        consumer = Consumer({
            'bootstrap.servers': 'host.docker.internal:9092',
            'group.id': 'airflow-consumer',
            'auto.offset.reset': 'earliest'
        })

        consumer.subscribe(['crypto-prices'])

        msg = consumer.poll(timeout=10.0)
        data = None
        if msg is None:
            print("❌ No message received.")
        elif msg.error():
            print("❌ Consumer error:", msg.error())
        else:
            data = json.loads(msg.value().decode('utf-8'))
            print("✅ Extracted:", data)

        consumer.close()
        return data

    @task()
    def transform(data: dict):
        if not data:
            return None
        data['bitcoin'] = round(data['bitcoin'], 2)
        data['ethereum'] = round(data['ethereum'], 2)
        print("🔁 Transformed:", data)
        return data

    @task()
    def load(data: dict):
        if not data:
            print("⚠️ No data to load.")
            return

        os.makedirs('/usr/local/airflow/data', exist_ok=True)
        file_path = '/usr/local/airflow/data/crypto_prices.csv'
        with open(file_path, 'a', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['timestamp', 'bitcoin', 'ethereum'])
            if os.stat(file_path).st_size == 0:
                writer.writeheader()
            writer.writerow(data)
        print("✅ Loaded to CSV:", data)

    # Define DAG execution flow
    load(transform(extract()))
