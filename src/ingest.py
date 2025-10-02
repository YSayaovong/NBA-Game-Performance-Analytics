# src/ingest.py
from pathlib import Path
import json
from time import sleep
from nba_api.stats.endpoints import teamgamelog
from nba_api.stats.static import teams

def fetch_team_game_logs(season: str, outdir: Path) -> Path:
    """
    Download each team's regular-season game logs for the given season (e.g., '2022-23')
    and save as JSON per team. Returns the raw data folder.
    """
    outdir.mkdir(parents=True, exist_ok=True)

    for t in teams.get_teams():
        team_id = t["id"]
        team_abbrev = t["abbreviation"]
        tg = teamgamelog.TeamGameLog(team_id=team_id, season=season, season_type_all_star="Regular Season")
        df = tg.get_data_frames()[0]
        payload = {
            "team_id": team_id,
            "abbreviation": team_abbrev,
            "season": season,
            "records": df.to_dict(orient="records"),
        }
        with (outdir / f"{team_abbrev}_{season.replace('-', '')}.json").open("w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
        sleep(0.6)  # polite pacing
    return outdir
