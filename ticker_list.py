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
    **{t: "Equities" for t in [
        "SPY","IWM","QQQ","DIA","ZSP.TO","XIU.TO","EFA","EEM",
        "XLE","XLF","XLV","XLI","XLK","XLC","XLY","XLP","XLRE","XLU","XMA.TO","ZUT.TO","JEPI"
    ]},
    **{t: "Bonds" for t in ["IEF","TLT","AGG","LQD","HYG","TIP","ZAG.TO","XCB.TO","XBB.TO","VGV.TO","HYDB"]},
    "SHY": "Cash",
    **{t: "Commodities" for t in ["GLD","SLV","CPER","DBC","USO","URA","PPL.TO","COW.TO","PDBC","DBMF","PHYS.TO","PSLV.TO"]},
    **{t: "Alternatives" for t in ["VNQ","XRE.TO","BTC-USD","ETH-USD","U-UN.TO"]}
}

groups = ["Equities", "Bonds", "Commodities", "Cash", "Alternatives"]