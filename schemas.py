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

    