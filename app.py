from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from optimizer_engine import run_optimizer  # your optimizer function
from datetime import datetime, timezone
from fetch_data import fetch_prices


app = FastAPI()

# Define input schema
class MacroInput(BaseModel):
    macro_regime: str
    summary: str
    proposed_strategy: Optional[str] = None
    equities: Optional[str] = None
    Bonds: Optional[str] = None
    Commodities: Optional[str] = None
    Cash: Optional[str] = None
    Alternatives: Optional[str] = None


@app.post("/parse")
async def parse(data: MacroInput):
    try:
        # --- Step 1: Build Outlook Dictionary ---
        outlook = {
            "Equities": data.equities or "medium",
            "Bonds": data.Bonds or "medium",
            "Commodities": data.Commodities or "medium",
            "Cash": data.Cash or "low",
            "Alternatives": data.Alternatives or "low",
        }

        # --- Step 2: Run the optimizer using that outlook ---
        result = run_optimizer(outlook)

        # --- Step 3: Attach metadata and return ---
        timestamp = datetime.now(timezone.utc).isoformat()

        return {
            "status": "success",
            "timestamp": timestamp,
            "macro_regime": data.macro_regime,
            "summary": data.summary,
            "proposed_strategy": data.proposed_strategy,
            "outlook": outlook,  # 👈 return outlook explicitly
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
    try:
        outlook = {
            "Equities": data.equities or "medium",
            "Bonds": data.Bonds or "medium",
            "Commodities": data.Commodities or "medium",
            "Cash": data.Cash or "low",
            "Alternatives": data.Alternatives or "low",
        }
        result = run_optimizer(outlook)
        return result
    except Exception as e:
        return {"status": "error", "message": str(e)}

    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
        }
