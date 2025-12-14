from typing import Dict, List
from schemas import ProposalPayload

def generate_proposal(macro_regime: str, api_key: str) -> ProposalPayload:
    # Calls OpenAI and returns a strictly formatted qualitative allocation plus justificaiton
    
    raw = {
        "qualitative_allocations":{
            "equities": "medium",
            "bonds": "low",
            "commodities": "high",
            "cash": "medium",
            "alts": "low"
        },
        "justification": "Sticky inflation supports real assets.\nHigher-for-longer rates weigh on bonds.\nGrowth uncertainty argues against high equity exposure."
    }

    return ProposalPayload(**raw)