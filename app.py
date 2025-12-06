import sys
print("PYTHON VERSION:", sys.version)
print("STARTING APP IMPORT...")

from datetime import datetime, timezone
from typing import Dict, Optional

from fastapi import FastAPI

print("IMPORTING fetch_data...")
from fetch_data import fetch_prices

print("IMPORTING optimizer_engine...")
from optimizer_engine import run_optimizer

print("APP IMPORT COMPLETED")

from pydantic import BaseModel

from fetch_data import fetch_prices
from optimizer_engine import run_optimizer

app = FastAPI()


class MacroInput(BaseModel):
    macro_regime: str
    summary: str
    proposed_strategy: Optional[str] = None
    equities: Optional[str] = None
    Bonds: Optional[str] = None
    Commodities: Optional[str] = None
    Cash: Optional[str] = None
    Alternatives: Optional[str] = None


def build_outlook(payload: MacroInput) -> Dict[str, str]:
    # Standardize qualitative inputs into the structure the optimizer expects
    return {
        "Equities": payload.equities or "medium",
        "Bonds": payload.Bonds or "medium",
        "Commodities": payload.Commodities or "medium",
        "Cash": payload.Cash or "low",
        "Alternatives": payload.Alternatives or "low",
    }

@app.get("/")
def root():
    return {"status": "ok", "message": "Optimizer backend running"}

@app.post("/parse")
async def parse(data: MacroInput):
    outlook = build_outlook(data)

    try:
        result = run_optimizer(outlook)
    except Exception as e:
        return {"status": "error", "message": str(e)}

    timestamp = datetime.now(timezone.utc).isoformat()

    return {
        "status": "success",
        "timestamp": timestamp,
        "macro_regime": data.macro_regime,
        "summary": data.summary,
        "proposed_strategy": data.proposed_strategy,
        "outlook": outlook,
        "optimization_result": result,
    }


@app.post("/refresh_data")
async def refresh_data():
    try:
        prices = fetch_prices()
        return {"status": "success", "rows": len(prices)}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@app.post("/optimize")
async def optimize(data: MacroInput):
    outlook = build_outlook(data)

    try:
        return run_optimizer(outlook)
    except Exception as e:
        return {"status": "error", "message": str(e)}
