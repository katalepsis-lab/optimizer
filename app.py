
"""
app.py

Defines a FastAPI backend for a macro-driven portfolio optimizer:

Initializes a FastAPI backend for the optimizer

Provides a health-check root endpoint

Exposes /proposal to generate AI-driven qualitative allocations and justification

Assigns a unique proposal ID and timestamp

Exposes /optimize to run the portfolio optimizer on validated inputs

Standardizes optimizer outputs via response models

Exposes /refresh_data to refresh and report cached market data

Uses HTTP exceptions for error handling

@Katalepsis-Lab 2025
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime, timezone
from ai_proposal import generate_proposal
from fetch_data import fetch_prices, CACHE_PATH
from optimizer_engine import run_optimizer
from schemas import OptimizeRequest, OptimizeResponse
import uuid
import os

app = FastAPI(title="Katalepsis Optimizer API")

@app.get("/")
def root():
    return {
        "status":"ok",
        "service":"optimizer-backend"
    }


class ProposalRequest(BaseModel):
    api_key: str
    macro_regime: str

class ProposalResponse(BaseModel):
    proposal_id: str
    qualitative_allocations: dict
    justification: str
    created_at: str


@app.post("/proposal", response_model=ProposalResponse)
def proposal(data: ProposalRequest):
    # Feed regime to API, receive allocations and justifications from ai_proposal.py
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
    # Send user validated qualitative asset allocation to optimizer and send back asset weights
    result = run_optimizer(data.qualitative_allocations.model_dump())

    return {
        "proposal_id": data.proposal_id,
        **result
    }

@app.post('/refresh_data')
def refresh_data():
    try:
        prices = fetch_prices()

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    if prices is None or prices.empty:
        raise HTTPException(
            status_code=500,
            detail='Price fetch failed or return empty dataset'
        )
    
    return {
        "status": "success",
        "rows": prices.shape[0],
        "tickers": prices.shape[1],
        "cache_path": CACHE_PATH,
    }