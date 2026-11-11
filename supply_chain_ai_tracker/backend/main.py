import asyncio
import json
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from motor.motor_asyncio import AsyncIOMotorClient
from .config import settings
from .db import get_collection
from .kafka_consumer import start_kafka_consumer
from .routes import shipments, documents

app = FastAPI(title="Supply Chain AI Tracker Backend")

# Include router modules
app.include_router(shipments.router, prefix="/api/shipments")
app.include_router(documents.router, prefix="/api/documents")

# Store connected websockets
class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@app.on_event("startup")
async def startup_event():
    # Start background Kafka consumer which will push updates via manager.broadcast
    asyncio.create_task(start_kafka_consumer(manager))

@app.websocket("/ws/transit")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()  # keep connection alive; client may send ping
    except WebSocketDisconnect:
        manager.disconnect(websocket)

# Simple health check
@app.get("/health")
async def health():
    return {"status": "ok"}
