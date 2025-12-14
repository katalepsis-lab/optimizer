from typing import Dict, List

def generate_proposal(macro_regime: str, api_key: str) -> Dict:
    # Calls OpenAI and returns a strictly formatted qualitative allocation plus justificaiton
    
    # Placeholder until wired to OpenAI
    return {
        "qualitative_allocations":{
            "equities": "medium",
            "bonds": "low",
            "commodities": "high",
            "cash": "medium",
            "alts": "low"
        },
        "justification": "Sticky inflation supports real assets.\nHigher-for-longer rates weigh on bonds.\nGrowth uncertainty argues against high equity exposure."
    }