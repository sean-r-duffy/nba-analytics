import pandas as pd
import numpy as np


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
