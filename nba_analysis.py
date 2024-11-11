import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from nba_api.stats.endpoints import leaguegamefinder

# Step 1: Retrieve NBA game data for the 2022-23 season
gamefinder = leaguegamefinder.LeagueGameFinder(season_nullable='2022-23')
games = gamefinder.get_data_frames()[0]

# Debugging Step: Check if data was retrieved successfully
print("First 5 rows of the games data:")
print(games.head())  # Display the first 5 rows to ensure data retrieval

# Define a list of official NBA teams to filter out All-Star or non-standard games
nba_teams = [
    "Atlanta Hawks", "Boston Celtics", "Brooklyn Nets", "Charlotte Hornets", "Chicago Bulls",
    "Cleveland Cavaliers", "Dallas Mavericks", "Denver Nuggets", "Detroit Pistons", "Golden State Warriors",
    "Houston Rockets", "Indiana Pacers", "LA Clippers", "Los Angeles Lakers", "Memphis Grizzlies",
    "Miami Heat", "Milwaukee Bucks", "Minnesota Timberwolves", "New Orleans Pelicans", "New York Knicks",
    "Oklahoma City Thunder", "Orlando Magic", "Philadelphia 76ers", "Phoenix Suns", "Portland Trail Blazers",
    "Sacramento Kings", "San Antonio Spurs", "Toronto Raptors", "Utah Jazz", "Washington Wizards"
]

# Filter data to include only rows where TEAM_NAME is in nba_teams
games = games[games['TEAM_NAME'].isin(nba_teams)]

# Debugging Step: Confirm filtering by printing unique team names in the filtered data
print("\nUnique team names after filtering:")
print(games['TEAM_NAME'].unique())

# Select relevant columns and check if all required columns are present
expected_columns = ['GAME_DATE', 'TEAM_NAME', 'PTS', 'FG_PCT', 'REB', 'AST']
missing_columns = [col for col in expected_columns if col not in games.columns]
if missing_columns:
    print(f"\nMissing columns: {missing_columns}")
else:
    # Proceed with the data selection if all columns are present
    games = games[expected_columns]
    games['GAME_DATE'] = pd.to_datetime(games['GAME_DATE'])

# Group by team and calculate average points, then sort and filter the top 10 teams
team_avg_points = games.groupby('TEAM_NAME')['PTS'].mean().sort_values(ascending=False).head(10)

# Plotting with adjustments for readability
plt.figure(figsize=(10, 6))  # Adjust figure size
sns.barplot(x=team_avg_points.values, y=team_avg_points.index, palette="viridis")
plt.title("Top 10 NBA Teams by Average Points in 2022-23 Season (Excluding All-Star Games)")
plt.xlabel("Average Points")
plt.ylabel("Team")
plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for readability
plt.show()
