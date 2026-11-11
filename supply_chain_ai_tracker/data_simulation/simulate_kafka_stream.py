import time
import json
import os
from datetime import datetime, timezone
from kafka import KafkaProducer
from pathlib import Path

# Load environment variables from .env if present
from dotenv import load_dotenv
load_dotenv()

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "transit_updates")

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def generate_message() -> dict:
    shipment_id = f"SHIP-{random.randint(1000, 9999)}"
    lat = round(random.uniform(-90, 90), 6)
    lng = round(random.uniform(-180, 180), 6)
    status = random.choice(["in_transit", "delayed", "arrived", "customs_hold"])
    timestamp = datetime.now(timezone.utc).isoformat()
    return {
        "shipment_id": shipment_id,
        "lat": lat,
        "lng": lng,
        "status": status,
        "timestamp": timestamp,
    }

def main():
    print(f"Starting Kafka load simulator → {KAFKA_BOOTSTRAP_SERVERS}, topic={KAFKA_TOPIC}")
    try:
        while True:
            msg = generate_message()
            producer.send(KAFKA_TOPIC, msg)
            # Aim for ~5,000 msgs/min ≈ 83 msgs/sec
            producer.flush()
            # Simple sleep to control rate
            time.sleep(0.012)  # ~83 Hz
    except KeyboardInterrupt:
        print("Simulator stopped by user.")

if __name__ == "__main__":
    main()
