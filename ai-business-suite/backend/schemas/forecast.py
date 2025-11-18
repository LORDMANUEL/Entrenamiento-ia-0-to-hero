from pydantic import BaseModel, Field
from typing import List

class MonthHistory(BaseModel):
    month: str = Field(..., example="2024-10", description="Month in YYYY-MM format")
    quantity: float = Field(..., ge=0, example=150.0, description="Sales quantity for the month")

class ForecastPredictionRequest(BaseModel):
    item_code: str = Field(..., example="ITM001")
    whs_code: str = Field(..., example="WHS01")
    history_months: List[MonthHistory]

class ForecastPredictionResponse(BaseModel):
    predicted_quantity: float = Field(..., example=165.5)
    model_version: str = Field(..., example="1.0.0")

class TopItem(BaseModel):
    item_code: str
    item_name: str
    whs_code: str
    predicted_quantity: float

class TopItemsResponse(BaseModel):
    top_items: List[TopItem]
