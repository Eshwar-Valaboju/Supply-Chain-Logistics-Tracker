#!/usr/bin/env bash
set -e

# 1. Start Docker services (MongoDB, Kafka, Zookeeper)
 echo "Starting Docker compose services..."
 docker-compose up -d

# Wait for services to become healthy (simple sleep, could be improved)
 echo "Waiting for services to be ready..."
 sleep 10

# 2. Install Python dependencies
 echo "Installing Python dependencies..."
 python -m pip install --upgrade pip
 pip install -r requirements.txt

# 3. Install Node dependencies and build frontend
 echo "Installing Node dependencies..."
 cd frontend
 npm install
 npm run dev &
 cd ..

# 4. Start FastAPI backend
 echo "Starting FastAPI backend..."
 uvicorn backend.main:app --host 0.0.0.0 --port 8000 &

# 5. Start Kafka load simulator (optional, runs in background)
 echo "Starting Kafka load simulator..."
 python data_simulation/simulate_kafka_stream.py &

wait
