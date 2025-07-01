from kafka import KafkaProducer 
import json, time 
import requests
from datetime import datetime 

producer = KafkaProducer(
    bootstrap_servers = "localhost:9092",
    value_serializer= lambda x: json.dumps(x).encode('utf-8')
)

def fetch_price():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd"
    response = requests.get(url).json()
    return {
        "timestamp" : datetime.now().isoformat(),
        "bitcoin" : response['bitcoin']['usd'],
        "ethereum" : response['ethereum']['usd']        
    }

while True:
    message = fetch_price()
    producer.send("crypto-prices", value = message)
    print("Sent:" , message)
    time.sleep(60)
