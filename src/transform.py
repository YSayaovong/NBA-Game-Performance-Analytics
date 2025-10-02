# src/transform.py
from pathlib import Path
import json
import pandas as pd
import numpy as np
import re

# Possession estimate (common heuristic)
# Poss = FGA - OREB + TOV + 0.44 * FTA
def estimate_possessions(row):
    return (row.get("FGA", 0) - row.get("OREB", 0) + row.get("TOV", 0) + 0.44 * row.get("FTA", 0))

def extract_opponent(matchup: str) -> str:
    if not isinstance(matchup, str):
        return None
    # Formats like 'BOS vs. PHI' or 'BOS @ MIA'
    m = re.search(r"vs\.\s+(\w+)|@\s+(\w+)", matchup)
    if not m:
        return None
    return m.group(1) or m.group(2)

def load_and_engineer(rawdir: Path, processed_path: Path) -> pd.DataFrame:
    frames = []
    for jf in rawdir.glob("*.json"):
        with jf.open("r", encoding="utf-8") as f:
            js = json.load(f)
        df = pd.DataFrame(js["records"]).copy()
        df["TEAM_ABBREV"] = js["abbreviation"]
        frames.append(df)

    if not frames:
        raise RuntimeError("No raw JSON files found. Run ingest first.")

    df = pd.concat(frames, ignore_index=True)

    # Ensure numeric where applicable
    num_cols = ["PTS","FGA","FTA","OREB","DREB","REB","AST","STL","BLK","TOV","PLUS_MINUS","FGM","FG3M","FG3A","FTM"]
    for c in num_cols:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")

    # Opponent code from MATCHUP (e.g., 'BOS vs. PHI' -> 'PHI')
    df["OPP"] = df["MATCHUP"].apply(extract_opponent)

    # Possessions and ratings
    df["POSS"] = df.apply(estimate_possessions, axis=1).clip(lower=1)

    # Merge to get opponent points per GAME_ID
    opp_pts = df[["GAME_ID","TEAM_ABBREV","PTS"]].rename(columns={"TEAM_ABBREV":"OPP","PTS":"OPP_PTS"})
    df = df.merge(opp_pts, on=["GAME_ID","OPP"], how="left" )

    # Ratings per game (per 100 poss)
    df["ORTG"] = 100.0 * df["PTS"] / df["POSS"]
    df["DRTG"] = 100.0 * df["OPP_PTS"] / df["POSS"]
    df["NETRTG"] = df["ORTG"] - df["DRTG"]
    df["WIN"] = (df["WL"] == "W").astype(int)

    # Team-level aggregates
    team_grp = df.groupby("TEAM_ABBREV", as_index=False).agg(
        GP=("GAME_ID","nunique"),
        WIN=("WIN","mean"),
        ORTG=("ORTG","mean"),
        DRTG=("DRTG","mean"),
        NETRTG=("NETRTG","mean"),
        TOV=("TOV","mean"),
        DREB=("DREB","mean")
    )
    team_grp["WIN_PCT"] = team_grp["WIN"].round(3)

    # Strength of schedule (simple): avg opponent WIN_PCT faced
    opp_win_pct = df.groupby("TEAM_ABBREV")["WIN"].mean()
    df["OPP_WIN_PCT"] = df["OPP"].map(opp_win_pct)
    sos = df.groupby("TEAM_ABBREV")["OPP_WIN_PCT"].mean().reset_index().rename(columns={"OPP_WIN_PCT":"SOS"})
    out = team_grp.merge(sos, on="TEAM_ABBREV", how="left")

    processed_path.parent.mkdir(parents=True, exist_ok=True)
    out.to_parquet(processed_path, index=False)
    return out
