import os
import json
import asyncio
from kafka import KafkaConsumer
from .config import settings
from .db import get_collection

async def consume_messages(manager):
    consumer = KafkaConsumer(
        settings.kafka_topic,
        bootstrap_servers=settings.kafka_bootstrap_servers,
        group_id=settings.kafka_group_id,
        value_deserializer=lambda m: json.loads(m.decode('utf-8')),
        enable_auto_commit=True,
        auto_offset_reset='earliest'
    )
    collection = get_collection('shipments')
    loop = asyncio.get_event_loop()
    for message in consumer:
        data = message.value
        # Upsert shipment document by shipment_id
        await collection.update_one(
            {"shipment_id": data["shipment_id"]},
            {"$set": data},
            upsert=True
        )
        # Broadcast to websockets
        await manager.broadcast(json.dumps(data))

async def start_kafka_consumer(manager):
    await consume_messages(manager)
