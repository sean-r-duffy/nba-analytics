from src.data import load, clean

data_dir = 'data'
external_dir = f'{data_dir}/external'
interim_dir = f'{data_dir}/interim'
processed_dir = f'{data_dir}/processed'

# Loading
load.scrape_stathead_players(external_dir)
load.scrape_stathead_teams(external_dir)
load.scrape_combine(external_dir)
load.download_kaggle_sets(external_dir)

# Cleaning
clean.clean_team_stats('data/external/NBA_team_stats_1979-2024.csv', interim_dir)
clean.clean_combine_data('data/external/NBA_combine_stats_2000-2024.csv', interim_dir)
clean.process_player_data(kaggle1_dir='data/external/kaggle1',
                          kaggle2_dir='data/external/kaggle2',
                          output_dir=interim_dir)
clean.clean_player_data('data/interim/player_data_aggregated.csv', processed_dir)