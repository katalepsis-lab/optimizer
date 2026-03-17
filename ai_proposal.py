"""
ai_proposal.py

Defines a strict system prompt that frames the model as a macro portfolio strategist
Constrains outputs to qualitative allocations using only low, medium, or high
Forces coverage of all asset classes exactly once
Provides an explicit input–output example to anchor the response format
Calls the Anthropic Messages API with low temperature for consistency
Accepts a macro regime description as input
Returns a validated ProposalPayload by parsing model JSON through Pydantic

Katalepsis-lab 2025

"""

from schemas import ProposalPayload
import anthropic

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
    # Calls Anthropic and returns a strictly formatted qualitative allocation plus justification
    client = anthropic.Anthropic(api_key=api_key)

    response = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=512,
        system=SYSTEM_PROMPT + EXAMPLE,
        messages=[
            {"role": "user", "content": macro_regime}
        ],
        temperature=0.2
    )

    content = response.content[0].text.strip()

    # Strip markdown code fences if the model wraps its output
    if content.startswith("```"):
        content = content.split("```")[1]
        if content.startswith("json"):
            content = content[4:]
        content = content.strip()

    return ProposalPayload.model_validate_json(content)
