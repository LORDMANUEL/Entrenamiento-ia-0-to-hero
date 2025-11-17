from pydantic import BaseModel, Field
from typing import List, Optional

class TicketDescriptionRequest(BaseModel):
    descripcion: str = Field(..., min_length=10, example="El cliente informa que el motor hace un ruido extraño al acelerar.")

class TicketClassificationResponse(BaseModel):
    categoria_predicha: str = Field(..., example="MECANICO")
    score_confianza: float = Field(..., ge=0, le=1, example=0.85)
    model_version: str = Field(..., example="1.0.0")

class SuggestedSolution(BaseModel):
    resumen: str = Field(..., example="Revisar la correa de distribución y el tensor...")
    fuente_ticket_id: str = Field(..., example="TKT0123")
    similarity_score: float = Field(..., ge=0, le=1, example=0.92)

class TicketSuggestionResponse(BaseModel):
    categoria_predicha: str = Field(..., example="MECANICO")
    soluciones_sugeridas: List[SuggestedSolution]
    model_version: str = Field(..., example="1.0.0")
