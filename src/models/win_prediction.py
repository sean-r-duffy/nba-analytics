import joblib
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from src.models.nn_search import get_nba_projection


def get_df(player_df, team_df):
    # Collect player df
    if isinstance(player_df, pd.DataFrame):
        df = player_df.copy()
    elif isinstance(player_df, str):
        df = pd.read_csv(player_df)
    else:
        raise Exception('player_df must be a pandas DataFrame object or the path of a .csv')

    # Collect team df
    if isinstance(team_df, pd.DataFrame):
        team_df = team_df.copy()
    elif isinstance(team_df, str):
        team_df = pd.read_csv(team_df)
    else:
        raise Exception('team_df must be a pandas DataFrame object or the path of a .csv')

    return player_df, team_df


def return_roster_stats(player_df, team_df, players, team, years):
    player_df, team_df = get_df(player_df, team_df)
    player_df = get_nba_projection(players, years)
    pass


def agg_by_pos(player_df, team_df, save_file=False, use_pca=False, pca_model_path=None, output_dir=None):
    df, team_df = get_df(player_df, team_df)

    # Columns not containing player stats
    non_stats_columns = ['g', 'gs', 'mp', 'tm', 'season', 'player_id', 'player', ]

    # Offsetting data so that player performances are from previous season
    df = df.drop(columns=['Unnamed: 0', 'seas_id', 'age'])
    seasons_df = df[['season', 'tm', 'player_id']]
    offset_df = df.drop(columns=['tm'])
    offset_df['season'] = offset_df['season'] + 1
    df = pd.merge(seasons_df, offset_df, on=['season', 'player_id'])

    # Transforms stats columns into principal components
    if use_pca:
        assert isinstance(pca_model_path, str), 'Must include directory in which to save PCA model'
        scaler = StandardScaler()
        scaled_df = scaler.fit_transform(df.drop(columns=non_stats_columns))
        pca = PCA(n_components=30, random_state=41)
        pc_df = pca.fit_transform(scaled_df)
        joblib.dump(pca, f'{pca_model_path}/player_pca.pkl')
        df_subset = df[
            ['g', 'gs', 'mp', 'tm', 'season', 'player_id', 'player', 'pos_PG', 'pos_SG', 'pos_PF', 'pos_SF', 'pos_C']]
        df = pd.merge(df_subset.reset_index(), pd.DataFrame(pc_df).reset_index())
        df = df.drop(columns=['index'])
        df = df.rename(columns={x: str(x) for x in range(0, 30)})
        column_titles = [str(x) for x in range(0, 30)]
    else:
        stats_df = df.drop(columns=non_stats_columns)
        column_titles = stats_df.columns.tolist()
        column_titles = [x for x in column_titles if x not in ['pos_PG', 'pos_SG', 'pos_PF', 'pos_SF', 'pos_C']]

    # Reverse one-hot-encoding
    for pos in 'PG', 'SG', 'PF', 'SF', 'C':
        df[f'pos_{pos}1'] = df[f'pos_{pos}'].apply(lambda x: pos if x else '')
    df['pos'] = df['pos_PG1'] + df['pos_SG1'] + df['pos_PF1'] + df['pos_SF1'] + df['pos_C1']
    df = df.drop(columns=['pos_PG1', 'pos_SG1', 'pos_PF1', 'pos_SF1', 'pos_C1'])
    df = df.drop(columns=['pos_PG', 'pos_SG', 'pos_PF', 'pos_SF', 'pos_C'])

    # Aggregating player data to weighted average by position
    total_min = df.groupby(by=['tm', 'season', 'pos']).sum()
    total_min = total_min.reset_index()[['tm', 'season', 'pos', 'mp']]
    total_min = total_min.rename(columns={'mp': 'total_mp'})
    df = pd.merge(df, total_min, on=['tm', 'season', 'pos'])
    df['mp%'] = df['mp'] / df['total_mp']
    for x in column_titles:
        df[x] = df[x] * df['mp%']
    df = df.groupby(by=['tm', 'season', 'pos']).sum()
    df = df.reset_index().drop(columns=['g', 'gs', 'mp', 'total_mp', 'mp%', 'player_id', 'player'])

    c_df = df[df['pos'] == 'C']
    pg_df = df[df['pos'] == 'PG']
    sg_df = df[df['pos'] == 'SG']
    pf_df = df[df['pos'] == 'PF']
    sf_df = df[df['pos'] == 'SF']
    df = pd.merge(c_df, pg_df, on=['tm', 'season'], suffixes=('C', 'PG'))
    df = pd.merge(df, sg_df, on=['tm', 'season'])
    df = pd.merge(df, pf_df, on=['tm', 'season'], suffixes=('SG', 'PF'))
    df = pd.merge(df, sf_df, on=['tm', 'season'])
    df = df.rename(columns={x: f'{x}SF' for x in column_titles})
    df = df.drop(columns=['pos', 'posC', 'posPG', 'posSG', 'posPF'])

    # Add win%
    team_df = team_df[['Season', 'Team', 'W%']]
    team_df = team_df.rename(columns={'Season': 'season', 'Team': 'tm'})
    df = pd.merge(df, team_df, on=['season', 'tm'])
    df = df.drop(columns=['tm', 'season'])

    if save_file:
        assert isinstance(output_dir, str), 'Must provide directory in which to save output .csv file'
        df.to_csv(f'{output_dir}/roster_win%.csv')

    return df
