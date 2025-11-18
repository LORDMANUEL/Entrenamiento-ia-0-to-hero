from pydantic import BaseModel, Field, validator
from typing import Optional

class RiskScoringRequest(BaseModel):
    customer_id: Optional[str] = Field(None, example="CUST-501")
    segment: str = Field(..., example="Retail")
    city: str = Field(..., example="Barcelona")
    amount: float = Field(..., gt=0, example=5000.0)
    payment_terms_days: int = Field(..., ge=0, example=30)
    past_due_count: int = Field(..., ge=0, example=2)
    avg_days_past_due: float = Field(..., ge=0, example=5.5)

    @validator('segment')
    def segment_must_be_valid(cls, v):
        valid_segments = ['Retail', 'Empresa', 'Gobierno']
        if v not in valid_segments:
            raise ValueError(f'segment must be one of {valid_segments}')
        return v

class RiskScoringResponse(BaseModel):
    prob_riesgo: float = Field(..., ge=0, le=1, example=0.45)
    bucket: str = Field(..., example="MEDIO")
    explanation: str = Field(..., example="Riesgo moderado. Factores como el monto o historial de pagos requieren atención.")
    model_version: str = Field(..., example="1.0.0")
