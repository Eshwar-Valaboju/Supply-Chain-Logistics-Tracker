"""API endpoints for handling unstructured logistics documents.

- POST /upload: Accept raw text, run the LangChain extractor, store the structured result.
- GET /entities: Return all extracted entities.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..db import get_collection
from ..ai.langchain_extractor import extract_shipment_entities

router = APIRouter()

class DocumentRequest(BaseModel):
    text: str

@router.post("/upload", response_model=dict)
async def upload_document(req: DocumentRequest):
    try:
        entity = extract_shipment_entities(req.text)
        # Convert Pydantic model to dict for storage
        data = entity.dict()
        # Store in a separate collection for extracted entities
        await get_collection("extracted_entities").insert_one(data)
        return {"status": "success", "entity": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/entities", response_model=list[dict])
async def list_entities():
    cursor = get_collection("extracted_entities").find({})
    result = []
    async for doc in cursor:
        doc["id"] = str(doc.get("_id"))
        result.append(doc)
    return result
