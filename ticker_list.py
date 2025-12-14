# ....................................................................
# 50 tickers for MVP
# ....................................................................

tickers = [
# Equities
    "SPY","IWM","QQQ","DIA","ZSP.TO","XIU.TO","EFA","EEM",
    # Bonds
    "XLE","XLF","XLV","XLI","XLK","XLC","XLY","XLP","XLRE","XLU","XMA.TO","ZUT.TO",
    # Cash
    "IEF","TLT","SHY","AGG","LQD","HYG","TIP","ZAG.TO","XCB.TO","XBB.TO","VGV.TO","HYDB",
    # Commodities
    "GLD","SLV","CPER","DBC","USO","URA","PPL.TO","COW.TO","PSLV.TO","PHYS.TO","U-UN.TO",
    # Alternatives
    "VNQ","XRE.TO","BTC-USD","ETH-USD","DBMF","PDBC","JEPI"
]

# Group assignment
group_map = {
    **{t: "equities" for t in [
        "SPY","IWM","QQQ","DIA","ZSP.TO","XIU.TO","EFA","EEM",
        "XLE","XLF","XLV","XLI","XLK","XLC","XLY","XLP","XLRE","XLU","XMA.TO","ZUT.TO","JEPI"
    ]},
    **{t: "bonds" for t in ["IEF","TLT","AGG","LQD","HYG","TIP","ZAG.TO","XCB.TO","XBB.TO","VGV.TO","HYDB"]},
    "SHY": "cash",
    **{t: "commodities" for t in ["GLD","SLV","CPER","DBC","USO","URA","PPL.TO","COW.TO","PDBC","DBMF","PHYS.TO","PSLV.TO"]},
    **{t: "alts" for t in ["VNQ","XRE.TO","BTC-USD","ETH-USD","U-UN.TO"]}
}

groups = ["equities", "bonds", "commodities", "cash", "alts"]