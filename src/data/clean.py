import pandas as pd
import numpy as np


# TODO: Fix all relative paths
def clean_team_stats(df=None):
    if df is None:
        df = pd.read_csv('../../data/external/NBA_team_stats_1979-2024.csv')

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
    df.to_csv('../data/interim/NBA_team_stats_1979-2024_clean.csv')

    return df


def clean_combine_data(df=None):
    if df is None:
        df = pd.read_csv('../../data/external/NBA_combine_stats_2000-2024.csv')

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
    df.to_csv('../../data/interim/combine_stats_trimmed.csv')

    return df


def process_player_data():
    player_shooting_df = pd.read_csv('../../data/external/kaggle2/Player Shooting.csv')
    advanced_df = pd.read_csv('../../data/external/kaggle2/Advanced.csv')
    player_per100poss_df = pd.read_csv('../../data/external/kaggle2/Per 100 Poss.csv')
    player_info_df = pd.read_csv('../../data/external/kaggle1/csv/common_player_info.csv')

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

    df.to_csv('../../data/interim/player_data_aggregated.csv')


if __name__ == '__main__':
    clean_team_stats()
    clean_combine_data()
    process_player_data()
