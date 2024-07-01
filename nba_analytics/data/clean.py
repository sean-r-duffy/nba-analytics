import pandas as pd


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
