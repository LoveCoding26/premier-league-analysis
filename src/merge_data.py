"""
Convert WhoScored Excel file (15 sheets) to 3 CSV files
- team_overall_stats.csv
- team_home_stats.csv
- team_away_stats.csv
"""

import pandas as pd
from pathlib import Path

# ==================== Path configuration ====================
SCRIPT_DIR = Path(__file__).parent.parent  # Project root directory

# Raw data location
EXCEL_PATH = SCRIPT_DIR / "data" / "raw" / "team_statistics.xlsx"

# Processed data location
PROCESSED_DIR = SCRIPT_DIR / "data" / "processed"

# Create output directory
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

# ==================== Check if file exists ====================
if not EXCEL_PATH.exists():
    raise FileNotFoundError(
        f"Cannot find data file: {EXCEL_PATH}\n"
        "Please ensure team_statistics.xlsx is placed in data/raw/ folder"
    )

print(f"[OK] Data file found: {EXCEL_PATH}")
print(f"[OK] Output directory: {PROCESSED_DIR}")

# ==================== Sheet mapping ====================
sheets_config = {
    "overall": {
        "summary": "summary_overall",
        "defensive": "defensive_overall",
        "offensive": "offensive_overall",
        "xG_for": "xG_overall_for",
        "xG_against": "xG_overall_against",
    },
    "home": {
        "summary": "summary_home",
        "defensive": "defensive_home",
        "offensive": "offensive_home",
        "xG_for": "xG_home_for",
        "xG_against": "xG_home_against",
    },
    "away": {
        "summary": "summary_away",
        "defensive": "defensive_away",
        "offensive": "offensive_away",
        "xG_for": "xG_away_for",
        "xG_against": "xG_away_against",
    },
}

def clean_team_name(team_str):
    """Extract team name, remove leading number like '1. Liverpool' -> 'Liverpool'"""
    if pd.isna(team_str):
        return team_str
    if ". " in str(team_str):
        return str(team_str).split(". ", 1)[1]
    return str(team_str)

def load_and_merge_dimension(excel_path, dimension_config, dimension_name):
    """Load all sheets for a dimension (overall/home/away) and merge them"""
    merged_df = None
    
    for category, sheet_name in dimension_config.items():
        print(f"  Reading: {sheet_name}")
        df = pd.read_excel(excel_path, sheet_name=sheet_name)
        
        # Clean team names
        df["Team"] = df["Team"].apply(clean_team_name)
        
        # Add prefix to columns except 'Team' to avoid duplicate names
        if category != "summary":
            rename_cols = {col: f"{category}_{col}" for col in df.columns if col != "Team"}
            df = df.rename(columns=rename_cols)
        
        # Merge
        if merged_df is None:
            merged_df = df
        else:
            merged_df = pd.merge(merged_df, df, on="Team", how="outer")
    
    # Sort by team name
    merged_df = merged_df.sort_values("Team").reset_index(drop=True)
    
    # Save to CSV
    output_path = PROCESSED_DIR / f"team_{dimension_name}_stats.csv"
    merged_df.to_csv(output_path, index=False)
    print(f"  [SAVED] {output_path} ({len(merged_df)} teams)")
    
    return merged_df

# ==================== Run conversion ====================
print("=" * 50)
print("Converting WhoScored data...")
print("=" * 50)

print("\n1. Processing Overall data...")
overall_df = load_and_merge_dimension(EXCEL_PATH, sheets_config["overall"], "overall")

print("\n2. Processing Home data...")
home_df = load_and_merge_dimension(EXCEL_PATH, sheets_config["home"], "home")

print("\n3. Processing Away data...")
away_df = load_and_merge_dimension(EXCEL_PATH, sheets_config["away"], "away")

print("\n" + "=" * 50)
print(f"[DONE] Conversion complete! 3 CSV files saved to:")
print(f"   {PROCESSED_DIR}")
print("=" * 50)

# Preview first 5 rows (using correct column names)
print("\nPreview of team_overall_stats.csv (first 5 rows):")
# Get first 5 rows and show available columns
preview_cols = ["Team", "Goals", "xG_for_xG", "Rating"]
# Check which columns actually exist
existing_cols = [col for col in preview_cols if col in overall_df.columns]
print(overall_df.head()[existing_cols].to_string())