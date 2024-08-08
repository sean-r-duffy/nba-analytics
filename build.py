from src.data import load, clean

data_dir = 'data'
external_dir = f'{data_dir}/external'
interim_dir = f'{data_dir}/interim'
processed_dir = f'{data_dir}/processed'

# Loading
load.scrape_stathead_players(external_dir)
load.scrape_stathead_teams(external_dir)
load.download_kaggle_set(external_dir)

# Cleaning
clean.clean_team_stats('data/external/team_stats.csv', interim_dir)
clean.process_player_data_long(kaggle1_dir='data/external/kaggle1',
                               kaggle2_dir='data/external/kaggle2',
                               output_dir=interim_dir)
clean.clean_player_data_long('data/interim/player_data_aggregated.csv', processed_dir)