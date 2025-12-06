
import numpy as np
import pandas as pd
from scipy.optimize import minimize
from pandas_datareader import data as pdr
import json
from datetime import datetime, timedelta, timezone
from ticker_list import tickers, group_map, groups
from fetch_data import CACHE_PATH
import os

# Qualitative to quantitative bounds
ranges = {"low": (0.00, 0.10), "medium": (0.10, 0.35), "high": (0.35, 0.70)}

# ....................................................................
# Optimizer function
# ....................................................................
def run_optimizer(outlook: dict) -> dict:
    
    if not os.path.exists(CACHE_PATH):
        raise FileNotFoundError("No price cache found. Call /refresh_data first.")
    
    # Use for performance evaluation
    start_time = datetime.now()
    print(f"\n Optimizer started at: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")

    # Load cached data
    prices = pd.read_parquet(CACHE_PATH)
    print(f"\n Loaded cached data with {prices.shape[1]} tickers and {prices.shape[0]} rows.")

    # Compute returns, covariance, and expected returns
    returns = prices.pct_change(fill_method=None).dropna(how="all").fillna(0)
    mu = returns.mean() * 252           # Yearly mean returns
    sigma = returns.cov() * 252         # Yearly covariance matrix

    # Risk-free rate from FRED
    end = datetime.today()
    start = end - timedelta(days=30)
    rf_df = pdr.DataReader("DTB3", "fred", start, end)
    rf = rf_df.iloc[-1, 0] / 100
    print(f"Risk-free rate (3-month T-bill): {rf:.2%}")

    # Convert qualitative outlook to min/max bounds per asset-class
    group_bounds = {g: ranges[outlook[g]] for g in groups}
    print("Group bounds:")
    for g in groups:
        print(f"  {g:12s}: {group_bounds[g][0]*100:5.1f}% - {group_bounds[g][1]*100:5.1f}%")

    # Index tickers by group
    idx = {g: [i for i, t in enumerate(prices.columns) if group_map.get(t, "") == g] for g in groups}

    # Sharpe ratio inputs
    mu_vec = mu.loc[prices.columns].values
    sigma_mat = sigma.loc[prices.columns, prices.columns].values
    n = len(mu_vec)

    # Objective function: negative Sharpe ratio
    def neg_sharpe(w):
        r = np.dot(w, mu_vec)
        v = np.sqrt(np.dot(w, sigma_mat @ w))
        return -(r - rf) / v

    # Constraints
    bounds = [(0, 1) for i in range(n)]
    constraints = [{"type": "eq", "fun": lambda w: np.sum(w) - 1.0}]    # Sum of all weights == 1
    for g in groups:
        members = idx[g]
        if len(members) == 0:
            print(f"⚠️ No data for group {g}")
            continue
        min_, max_ = group_bounds[g]
        constraints.append({"type": "ineq", "fun": lambda w, I=members, lb=min_: np.sum(w[I]) - lb})    # Weights within class above lb
        constraints.append({"type": "ineq", "fun": lambda w, I=members, ub=max_: ub - np.sum(w[I])})    # Weights within class below ub

    # Optimization (minimize negative Sharpe Ratio)
    x0 = np.ones(n) / n     # Initial guess is equal weighted
    
    result = minimize(neg_sharpe, x0, bounds=bounds, constraints=constraints,
                      method="SLSQP", options={"maxiter": 5000, "disp": True})

    # Gathering optimization output
    w_opt = pd.Series(result.x, index=prices.columns)
    pf_ret = np.dot(w_opt, mu_vec)
    pf_vol = np.sqrt(np.dot(w_opt, sigma_mat @ w_opt))
    pf_sharpe = (pf_ret - rf) / pf_vol

    # Use for performance evaluation
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    print(f"Optimizer finished at: {end_time.strftime('%Y-%m-%d %H:%M:%S')} (Duration: {duration:.2f} seconds)")

    # Structured output
    result_json = {
        "expected_return": round(pf_ret, 3),
        "volatility": round(pf_vol, 3),
        "sharpe_ratio": round(pf_sharpe, 3),
        "weights": w_opt[w_opt > 1e-4].round(3).to_dict(),
        "engine_end_time": end_time.isoformat(),
        "engine_duration_sec": round(duration, 3)
    }

    return result_json


# ....................................................................
# Local testing
# ....................................................................

if __name__ == "__main__":
    test_outlook = {
        "Equities": "low",
        "Bonds": "high",
        "Commodities": "high",
        "Cash": "medium",
        "Alternatives": "low"
    }
    result = run_optimizer(test_outlook)
    print(json.dumps(result, indent=2))
