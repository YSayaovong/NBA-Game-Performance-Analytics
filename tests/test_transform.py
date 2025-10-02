# tests/test_transform.py
from pathlib import Path
import pandas as pd
from transform import estimate_possessions

def test_possessions_estimate_positive():
    row = {"FGA": 80, "OREB": 10, "TOV": 14, "FTA": 20}
    poss = estimate_possessions(row)
    assert poss > 0
