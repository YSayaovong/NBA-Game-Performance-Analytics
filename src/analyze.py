# src/analyze.py
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

def save_figures(df: pd.DataFrame, outdir: Path) -> None:
    outdir.mkdir(parents=True, exist_ok=True)

    # Bar: ORTG ranked
    df.sort_values("ORTG", ascending=False).plot(
        x="TEAM_ABBREV", y="ORTG", kind="bar", legend=False, figsize=(10,5), title="Offensive Rating (per 100) – 2022–23"
    )
    plt.tight_layout()
    plt.savefig(outdir / "rank_ortg.png")
    plt.close()

    # Bar: DRTG ranked (lower is better)
    df.sort_values("DRTG", ascending=True).plot(
        x="TEAM_ABBREV", y="DRTG", kind="bar", legend=False, figsize=(10,5), title="Defensive Rating (per 100) – 2022–23 (lower is better)"
    )
    plt.tight_layout()
    plt.savefig(outdir / "rank_drtg.png")
    plt.close()

    # Scatter: NetRtg vs Win%
    ax = df.plot(kind="scatter", x="NETRTG", y="WIN_PCT", figsize=(6,5), title="Net Rating vs Win% – 2022–23")
    for _, r in df.iterrows():
        ax.annotate(r["TEAM_ABBREV"], (r["NETRTG"], r["WIN_PCT"]), fontsize=7, xytext=(3,3), textcoords="offset points")
    plt.tight_layout()
    plt.savefig(outdir / "netrtg_vs_winpct.png")
    plt.close()

def compute_correlations(df: pd.DataFrame) -> pd.Series:
    cols = ["ORTG","DRTG","NETRTG","TOV","DREB","SOS","WIN_PCT"]
    return df[cols].corr()["WIN_PCT"].sort_values(ascending=False)
