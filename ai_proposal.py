from typing import Dict, List
from schemas import ProposalPayload
from openai import OpenAI

SYSTEM_PROMPT = """
You are an expert macro portfolio strategist with decades of experience in asset allocation.

Your task:
- Read a macroeconomic outlook
- Propose qualitative asset class allocations
- Use ONLY: "low", "medium", or "high"
- Cover ALL asset classes exactly once

Asset classes:
- equities
- bonds
- commodities
- cash
- alts

You MUST return valid JSON ONLY.
No markdown. No explanations outside JSON.

The JSON schema is:

{
  "qualitative_allocations": {
    "equities": "low|medium|high",
    "bonds": "low|medium|high",
    "commodities": "low|medium|high",
    "cash": "low|medium|high",
    "alts": "low|medium|high"
  },
  "justification": "concise macro justification"
}

"""

EXAMPLE = """
Example input:
"Growth is slowing, inflation remains elevated, central banks keep rates restrictive."

Example output:
{
  "qualitative_allocations": {
    "equities": "medium",
    "bonds": "low",
    "commodities": "high",
    "cash": "medium",
    "alts": "low"
  },
  "justification": "Sticky inflation favors real assets, while higher rates reduce bond attractiveness and argue for maintaining liquidity."
}
"""

def generate_proposal(macro_regime: str, api_key: str) -> ProposalPayload:
    # Calls OpenAI and returns a strictly formatted qualitative allocation plus justificaiton
    client = OpenAI(api_key=api_key)

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {'role': 'system', 'content': SYSTEM_PROMPT},
            {'role': 'system', 'content': EXAMPLE},
            {'role': 'user', 'content': macro_regime}
        ],
        temperature=0.2
    )
    
    content = response.choices[0].message.content

    return ProposalPayload.model_validate_json(content)