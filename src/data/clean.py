import pandas as pd
import numpy as np
from typing import Union
from src.data.load import get_df


def clean_team_stats(team_df: Union[pd.DataFrame, str],
                     output_dir: str,
                     filename: str = 'team_stats_clean.csv') -> pd.DataFrame:
    """
    Cleans raw stathead team data, writes to CSV, and returns cleaned DataFrame

    :param team_df: Path of CSV or DataFrame object of raw stathead team data
    :param output_dir: Directory in which to save CSV
    :param filename: Name of CSV file to save data to
    :return: Cleaned dataframe
    """

    # Get df if CSV was given
    df = get_df(team_df)

    # Establish headers and drop first column and row (unnecessary header and index)
    df.columns = df.iloc[0]
    df = df[1:]
    df = df.reset_index(drop=True)

    # Drop duplicate rows
    df = df.loc[:, ~df.columns.duplicated()]

    # Remove rows with invalid season and format Season column as int
    df = df[df['Season'] != 'Season']
    df['Season'] = df['Season'].map(lambda x: int(x[:4]))

    # Drop unnecessary columns
    df = df.drop(columns=['Rk'])

    # Convert all appropriate columns to numeric datatype
    df = df.apply(lambda col: pd.to_numeric(col, errors='coerce') if col.name != 'Team' else col)
    for column in ['MP', 'FG', 'FGA', '2P', '2PA', '3P', '3PA', 'FT', 'FTA', 'ORB', 'DRB', 'TRB', 'AST', 'STL', 'BLK',
                   'TOV', 'PF', 'PTS']:
        df[f'{column}/G'] = df[column] / df['G']
        df = df.drop(columns=[column])

    # Rename columns for clarity
    df = df.rename(columns={'W/L%': 'W%'})

    # Write results
    df.to_csv(f'{output_dir}/{filename}')

    return df


def clean_player_data_short(player_df: Union[pd.DataFrame, str],
                            all_star_df: Union[pd.DataFrame, str],
                            output_dir: str,
                            filename: str = 'player_stats_short.csv') -> pd.DataFrame:
    """
    Combines and cleans scraped stathead player and allstar data into single dataframe and writes result to CSV

    :param player_df: Path of CSV or DataFrame of raw stathead player data
    :param all_star_df: Path of CSV or DataFrame of raw stathead all-star data
    :param output_dir: Directory in which to save CSV
    :param filename: Name of CSV file to save data to
    :return: Cleaned dataframe
    """

    # Get DataFrames from CSVs if necessary
    players = get_df(player_df)
    all_stars = get_df(all_star_df)

    # If a player in the all players DataFrame is an all star, set value in All Star column = True
    all_stars = all_stars[['Player', 'Season']]
    all_stars['All Star'] = True
    df = pd.merge(players, all_stars, on=['Player', 'Season'], how='outer')

    # Fill All Star column value for non-all-stars as False
    df['All Star'] = df['All Star'].fillna(False)

    # Write results
    df.to_csv(f'{output_dir}/{filename}')

    return df


def process_player_data_long(kaggle1_dir: str,
                             kaggle2_dir: str,
                             output_dir: str,
                             filename: str = 'player_data_aggregated.csv') -> pd.DataFrame:
    """
    Combines player data from kaggle. Writes results to CSV and returns DataFrame

    :param kaggle1_dir: Path of directory containing kaggle data from 'wyattowalsh/basketball'
    :param kaggle2_dir: Path of directory containing kaggle data from 'sumitrodatta/nba-aba-baa-stats'
    :param output_dir: Directory in which to save CSV
    :param filename: Name of CSV file to save data to
    :return: Combined dataframe
    """

    # Paths of data from 'wyattowalsh/basketball'
    player_info_path = f'{kaggle1_dir}csv/common_player_info.csv'

    # Paths of data from 'sumitrodatta/nba-aba-baa-stats'
    shooting_stats_path = f'{kaggle2_dir}/Player Shooting.csv'
    advanced_stats_path = f'{kaggle2_dir}/Advanced.csv'
    per100poss_stats_path = f'{kaggle2_dir}/Per 100 Poss.csv'

    # Load all DataFrames
    player_info_df = pd.read_csv(player_info_path)
    player_shooting_df = pd.read_csv(shooting_stats_path)
    advanced_df = pd.read_csv(advanced_stats_path)
    player_per100poss_df = pd.read_csv(per100poss_stats_path)

    # Combine DataFrames
    df = pd.merge(player_per100poss_df, player_shooting_df,
                  on='seas_id',
                  how='inner',
                  suffixes=('', '_right'))
    df = pd.merge(df, advanced_df,
                  on='seas_id',
                  how='inner',
                  suffixes=('', '_right'))
    df = pd.merge(df, player_info_df,
                  left_on='player',
                  right_on='display_first_last',
                  how='inner',
                  suffixes=('', '_right'))

    # Drop duplicate columns, as indicated by presence of suffix
    df = df.loc[:, ~df.columns.str.endswith('_right')]

    # Write results
    df.to_csv(f'{output_dir}/{filename}')

    return df


def clean_player_data_long(combined_df: Union[pd.DataFrame, str],
                           output_dir: str,
                           filename: str = 'player_data_clean.csv') -> pd.DataFrame:
    """
    Cleans combined player data from Kaggle and returns cleaned DataFrame

    :param combined_df: Path of CSV or DataFrame of combined Kaggle player data
    :param output_dir: Directory in which to save CSV
    :param filename: Name of CSV file to save data to
    :return: Cleaned DataFrame
    """

    # Get DataFrame from CSV if necessary
    df = get_df(combined_df)

    # Drop unnecessary columns
    df = df.drop(columns=['Unnamed: 0', 'birth_year', 'birthdate', 'display_first_last', 'display_last_comma_first',
                          'display_fi_last', 'player_slug', 'season_exp', 'games_played_current_season_flag',
                          'team_id', 'team_name', 'team_abbreviation', 'team_code', 'team_city', 'playercode',
                          'dleague_flag', 'nba_flag', 'games_played_flag', 'greatest_75_flag', 'fg_percent',
                          'x3p_percent', 'x2p_percent', 'ft_percent', 'ts_percent', 'school', 'jersey', 'position',
                          'from_year', 'to_year', 'draft_round', 'draft_number', 'first_name', 'last_name', 'country',
                          'last_affiliation'])

    # Only keep players that played more than 10 games
    df = df[df['g'] >= 10]

    # Fill NaN values in percentage columns with 0. This means players that took no shots are shown the same as players
    # that missed all shots
    null_percent_columns = ['fg_percent_from_x2p_range', 'fg_percent_from_x0_3_range',
                            'fg_percent_from_x3_10_range', 'fg_percent_from_x10_16_range',
                            'fg_percent_from_x16_3p_range', 'fg_percent_from_x3p_range',
                            'percent_assisted_x2p_fg', 'percent_assisted_x3p_fg',
                            'percent_corner_3s_of_3pa', 'corner_3_point_percent']
    df[null_percent_columns] = df[null_percent_columns].fillna(0)

    # One hot encoding 'pos' feature
    df['pos_PG'] = df['pos'].apply(lambda x: 'PG' in x)
    df['pos_SG'] = df['pos'].apply(lambda x: 'SG' in x)
    df['pos_PF'] = df['pos'].apply(lambda x: 'PF' in x)
    df['pos_SF'] = df['pos'].apply(lambda x: 'SF' in x)
    df['pos_C'] = df['pos'].apply(lambda x: 'C' in x)

    # Can remove 'pos' below if original categorical feature is wanted along with encoding
    df = df.drop(columns=['pos', 'lg', 'draft_year', 'rosterstatus'])

    # Converting height to inches
    df = df.dropna(subset=['height', 'weight'])
    df['height_ft'] = df['height'].apply(lambda x: int(x.split('-')[0]))
    df['height_in'] = df['height'].apply(lambda x: int(x.split('-')[1]))
    df['height'] = (df['height_ft'] * 12) + df['height_in']
    df = df.drop(columns=['height_ft', 'height_in'])

    # Write results
    df.to_csv(f'{output_dir}/{filename}')

    return df


if __name__ == '__main__':
    # Directories in which to save outputs
    interim_dir = 'data/interim'
    processed_dir = 'data/processed'

    # Combine kaggle data into single player dataset
    process_player_data_long(kaggle1_dir='data/external/kaggle1',
                             kaggle2_dir='data/external/kaggle2',
                             output_dir=interim_dir)

    # Clean
    clean_team_stats('data/external/team_stats.csv', processed_dir)
    clean_player_data_long('data/interim/player_data_aggregated.csv', processed_dir)
    clean_player_data_short('data/external/all_player_stats_00-24.csv',
                            'data/external/allstar_stats_00-24.csv',
                            processed_dir)
