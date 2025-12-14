"""
schemas.py

Defines allowed qualitative buckets and asset class names as global constants

Implements QualitativeAllocation to enforce valid low, medium, high values per asset class

Uses a wildcard Pydantic field validator to validate all asset class fields uniformly

Raises explicit validation errors for invalid qualitative inputs

Defines ProposalPayload to bundle qualitative allocations with a macro justification

Defines OptimizerInput as a flat qualitative allocation structure for downstream processing

Defines OptimizeRequest to pass a proposal ID with validated qualitative allocations into the optimizer

Defines OptimizeResponse to standardize optimizer outputs including risk metrics, weights, and timing metadata


@Katalepsis-Lab 2025
"""



from pydantic import BaseModel, field_validator

ALLOWED_BUCKETS = {'low', 'medium', 'high'}
ASSET_CLASSES = {'equities', 'bonds', 'commodities', 'cash', 'alts'}

class QualitativeAllocation(BaseModel):
    # validating response for each asset class
    equities: str
    bonds: str
    commodities: str
    cash: str
    alts: str

    @field_validator("*")
    @classmethod
    
    def check_bucket(cls, i):
        if i not in ALLOWED_BUCKETS:
            raise ValueError(f'Invalid bucket: {i}')
        return i
    
class ProposalPayload(BaseModel):
    qualitative_allocations: QualitativeAllocation
    justification: str

class OptimizerInput(BaseModel):
    equities: str
    bonds: str
    commodities: str
    cash: str
    alts: str

class OptimizeResponse(BaseModel):
    proposal_id: str
    expected_return: float
    volatility: float
    sharpe_ratio: float
    weights: dict
    engine_end_time: str
    engine_duration_sec: float


class OptimizeRequest(BaseModel):
    proposal_id: str
    qualitative_allocations: QualitativeAllocation

    