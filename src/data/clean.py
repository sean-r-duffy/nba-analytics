import pandas as pd
import numpy as np


def clean_team_stats(df, output_dir):
    if isinstance(df, pd.DataFrame):
        pass
    elif isinstance(df, str):
        df = pd.read_csv(df)
    else:
        raise Exception('df must be a pandas DataFrame object or the path of a .csv')

    df.columns = df.iloc[0]
    df = df[1:]
    df = df.reset_index(drop=True)
    df = df.loc[:, ~df.columns.duplicated()]
    df = df[df['Season'] != 'Season']
    df['Season'] = df['Season'].map(lambda x: int(x[:4]))
    df = df.drop(columns=['Rk'])
    df = df.apply(lambda col: pd.to_numeric(col, errors='coerce') if col.name != 'Team' else col)
    for column in ['MP', 'FG', 'FGA', '2P', '2PA', '3P', '3PA', 'FT', 'FTA', 'ORB', 'DRB', 'TRB', 'AST', 'STL', 'BLK',
                   'TOV', 'PF', 'PTS']:
        df[f'{column}/G'] = df[column] / df['G']
        df = df.drop(columns=[column])
    df = df.rename(columns={'W/L%': 'W%'})
    df.to_csv(f'{output_dir}/NBA_team_stats_1979-2024_clean.csv')

    return df


def clean_combine_data(df, output_dir):
    if isinstance(df, pd.DataFrame):
        pass
    elif isinstance(df, str):
        df = pd.read_csv(df)
    else:
        raise Exception('df must be a pandas DataFrame object or the path of a .csv')

    def height_to_inches(height):
        if pd.isnull(height):
            return np.nan
        parts = height.split("'")
        feet = parts[0].strip()
        inches = parts[1].replace('"', '').strip()
        return int(feet) * 12 + float(inches)

    df.replace('-', np.nan, inplace=True)
    df.replace('-%', np.nan, inplace=True)
    df['height_wo_shoes'] = df['height_wo_shoes'].apply(height_to_inches)
    df['height_w_shoes'] = df['height_w_shoes'].apply(height_to_inches)
    df['standing_reach'] = df['standing_reach'].apply(height_to_inches)
    df['wingspan'] = df['wingspan'].apply(height_to_inches)
    df["bodyfat%"] = df["bodyfat%"].str.replace("%", "").astype('float')

    cols = ['bodyfat%', 'hand_len_in', 'hand_width_in',
            'height_wo_shoes', 'height_w_shoes', 'standing_reach', 'weight_lbs',
            'wingspan', 'lane_agility_s', 'shuttle_run_s', 'three_q_sprint_s',
            'standing_vert_in', 'max_vert_in', 'max_bench_reps']

    for col in cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    df = df.dropna(subset=cols, how='all').reset_index(drop=True)
    df.to_csv(f'{output_dir}/combine_stats_trimmed.csv')

    return df


def process_player_data(kaggle1_dir, kaggle2_dir, output_dir):
    player_shooting_df = pd.read_csv(f'{kaggle2_dir}/Player Shooting.csv')
    advanced_df = pd.read_csv(f'{kaggle2_dir}/Advanced.csv')
    player_per100poss_df = pd.read_csv(f'{kaggle2_dir}/Per 100 Poss.csv')
    player_info_df = pd.read_csv(f'{kaggle1_dir}csv/common_player_info.csv')

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

    df = df.loc[:, ~df.columns.str.endswith('_right')]

    df.to_csv(f'{output_dir}/player_data_aggregated.csv')


def clean_player_data(df, output_dir):
    if isinstance(df, pd.DataFrame):
        pass
    elif isinstance(df, str):
        df = pd.read_csv(df)
    else:
        raise Exception('df must be a pandas DataFrame object or the path of a .csv')

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

    df.to_csv(f'{output_dir}/processed/player_data_clean.csv')


if __name__ == '__main__':
    interim_dir = 'data/interim'
    processed_dir = 'data/processed'
    clean_team_stats('data/external/NBA_team_stats_1979-2024.csv', interim_dir)
    clean_combine_data('data/external/NBA_combine_stats_2000-2024.csv', interim_dir)
    process_player_data(kaggle1_dir='data/external/kaggle1',
                        kaggle2_dir='data/external/kaggle2',
                        output_dir=interim_dir)
    clean_player_data('data/interim/player_data_aggregated.csv', processed_dir)
