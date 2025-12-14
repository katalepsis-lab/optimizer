
"""
app.py

Defines a FastAPI backend for a macro-driven portfolio optimizer:
- Exposes endpoints to receive qualitative macro inputs
- Standardize them into asset-class outlooks
- Run an optimization engine
- Refresh market price data
- Return optimized portfolio results with timestamps and metadata.


Katalepsis-lab 2025
"""
from fastapi import FastAPI

app = FastAPI(title="Katalepsis Optimizer API")

@app.get("/")
def root():
    return {
        "status":"ok"
        "service":"optimizer-backend"
    }