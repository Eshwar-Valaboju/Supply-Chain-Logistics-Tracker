from pydantic import BaseModel, Field

class ShipmentEntitySchema(BaseModel):
    bill_of_lading_id: str = Field(..., description="Unique identifier of the bill of lading")
    delay_reason: str = Field(..., description="Reason for delay, e.g., customs, weather")
    estimated_delay_days: int = Field(..., ge=0, description="Estimated delay in days")
    critical_status: bool = Field(..., description="Whether the delay is critical for downstream operations")
