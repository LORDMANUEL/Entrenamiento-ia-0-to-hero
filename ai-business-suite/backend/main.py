from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.config import settings
from core.logging_config import setup_logging
from routers import forecast, risk_scoring, nlp_tickets

# Setup logging
setup_logging()

app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
)

# CORS configuration
origins = [
    "http://localhost:5173",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(forecast.router, prefix="/api/forecast", tags=["Forecast"])
app.include_router(risk_scoring.router, prefix="/api/risk", tags=["Risk Scoring"])
app.include_router(nlp_tickets.router, prefix="/api/tickets", tags=["NLP Tickets"])


@app.get("/api/health", tags=["Health"])
def health_check():
    """Health check endpoint."""
    return {"status": "ok"}

@app.get("/", include_in_schema=False)
def root():
    return {"message": "Welcome to the AI Business Suite API"}
