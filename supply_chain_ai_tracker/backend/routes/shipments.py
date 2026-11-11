from fastapi import APIRouter, Depends
from typing import List
from ..db import get_collection
from ..config import settings
from bson import ObjectId

router = APIRouter()

@router.get("/", response_model=List[dict])
async def list_shipments():
    """Return all shipment documents stored in MongoDB."""
    cursor = get_collection("shipments").find({})
    result = []
    async for doc in cursor:
        doc["id"] = str(doc.get("_id"))
        result.append(doc)
    return result

@router.get("/{shipment_id}", response_model=dict)
async def get_shipment(shipment_id: str):
    """Retrieve a single shipment by its ``shipment_id`` field."""
    doc = await get_collection("shipments").find_one({"shipment_id": shipment_id})
    if doc:
        doc["id"] = str(doc.get("_id"))
    return doc or {}
