
"""
app.py

Defines a FastAPI backend for a macro-driven portfolio optimizer:


Katalepsis-lab 2025
"""
from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime, timezone
from ai_proposal import generate_proposal
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
def proposal(data: ProposalRequest):
    # Feed regime and api, receive allocations and justifications from ai_proposal.py
    result = generate_proposal(
        macro_regime=data.macro_regime,
        api_key=data.api_key
    )

    return {
        "proposal_id": str(uuid.uuid4()),
        "qualitative_allocations": result.qualitative_allocations.model_dump(),
        "justification": result.justification,
        "created_at": datetime.now(timezone.utc).isoformat()
    }