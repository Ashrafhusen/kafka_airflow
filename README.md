# ⚡ Kafka + Airflow ETL Pipeline

A real-time ETL pipeline using **Apache Kafka** for data streaming and **Apache Airflow (Astro CLI)** for orchestration. Simulates cryptocurrency prices and stores processed results in a CSV file.

---

## 🔧 Tech Stack

- Kafka + Zookeeper  
- Airflow (Astro CLI, TaskFlow API)  
- Python  
- Docker + Docker Compose  
- CSV Output

---

## 🚀 Quick Start

```bash
# Start Kafka and Zookeeper
docker-compose -f docker-compose.kafka.yml up -d

# Start Airflow
astro dev start

# Run the producer
python producer/producer.py
