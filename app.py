
"""
app.py

Defines a FastAPI backend for a macro-driven portfolio optimizer:
- Exposes endpoints to receive qualitative macro inputs
- Standardize them into asset-class outlooks
- Run an optimization engine
- Refresh market price data
- Return optimized portfolio results with timestamps and metadata.


Katalepsis-lab 2025
"""
from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime, timezone
import uuid

app = FastAPI(title="Katalepsis Optimizer API")

@app.get("/")
def root():
    return {
        "status":"ok",
        "service":"optimizer-backend"
    }


class ProposalRequest(BaseModel):
    # First message received from front-end
    api_key: str
    macro_regime: str

class ProposalResponse(BaseModel):
    # First response to front-end
    proposal_id: str
    qualitative_allocations: dict
    justification: str
    created_at: str


@app.post("/proposal", response_model=ProposalResponse)
def proposal(body: ProposalRequest):
    return {
        "proposal_id": str(uuid.uuid4()),
        "qualitative_allocations": {
        "equities": "medium",
        "bonds": "medium",
        "commodities": "medium",
        "cash": "low",
        "alts": "low"
    },
    "justification": "This is the AI justification location",
    "created_at": datetime.now(timezone.utc).isoformat()
    }