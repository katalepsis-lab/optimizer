
"""
app.py

Defines a FastAPI backend for a macro-driven portfolio optimizer:


Katalepsis-lab 2025
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime, timezone
from ai_proposal import generate_proposal
from optimizer_engine import run_optimizer
from schemas import OptimizeRequest, OptimizeResponse
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
    try:
        payload = generate_proposal(
            macro_regime=data.macro_regime,
            api_key=data.api_key
        )
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e)
                            )
    return {
        "proposal_id": str(uuid.uuid4()),
        "qualitative_allocations": payload.qualitative_allocations.model_dump(),
        "justification": payload.justification,
        "created_at": datetime.now(timezone.utc).isoformat()
    }

@app.post("/optimize", response_model=OptimizeResponse)
def optimize(data: OptimizeRequest):
    result = run_optimizer(data.qualitative_allocations.model_dump())

    return {
        "proposal_id": data.proposal_id,
        "result":result
    }