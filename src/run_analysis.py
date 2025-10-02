# src/run_analysis.py
import argparse
from pathlib import Path
from ingest import fetch_team_game_logs
from transform import load_and_engineer
from analyze import save_figures, compute_correlations

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--season", default="2022-23", help='NBA season string, e.g., "2022-23"')
    args = p.parse_args()

    base = Path(__file__).resolve().parents[1]
    raw_dir = base / "data" / "raw"
    processed_path = base / "data" / "processed" / "team_metrics.parquet"
    figs_dir = base / "outputs" / "figures"

    print(f"Ingesting game logs for season {args.season} ...")
    fetch_team_game_logs(args.season, raw_dir)

    print("Transforming and engineering features ...")
    df = load_and_engineer(raw_dir, processed_path)
    print(f"Saved processed dataset to: {processed_path}")

    print("Saving figures ...")
    save_figures(df, figs_dir)
    print(f"Figures saved to: {figs_dir}")

    print("Key correlations with Win% (descending):")
    print(compute_correlations(df))

if __name__ == "__main__":
    main()
