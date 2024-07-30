import joblib
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from src.models.nn_search import get_nba_projection

def calculate_top_players_ui(selected_team: str, available_players:list) -> dict:
    # fill with model
    return {"Player": available_players[:4],
            "Win%": [.89, .78, .67, .45]}

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
    pass


def weighted_avg(group, weight_col, stat_cols):
    d = {}
    for col in stat_cols:
        d[col] = (group[col] * group[weight_col]).sum() / group[weight_col].sum()
    d[weight_col] = group[weight_col].sum()
    return pd.Series(d)

def weighted_avg_2(group, weight_col, stat_cols):
    d = {}
    for col in stat_cols:
        d[col] = (group[col] * group[weight_col]).sum() / group[weight_col].sum()
    return pd.Series(d)

def agg_by_pos(team_stats, player_stats):
    player_metrics = ["fg_per_100_poss", "fga_per_100_poss", "x3p_per_100_poss", "x3pa_per_100_poss", "x2p_per_100_poss", "x2pa_per_100_poss", "ft_per_100_poss", "fta_per_100_poss", "orb_per_100_poss", "drb_per_100_poss", "trb_per_100_poss", "ast_per_100_poss", "stl_per_100_poss", "blk_per_100_poss", "tov_per_100_poss", "pf_per_100_poss", "pts_per_100_poss", "o_rtg", "d_rtg", "avg_dist_fga", "percent_fga_from_x2p_range", "percent_fga_from_x0_3_range", "percent_fga_from_x3_10_range", "percent_fga_from_x10_16_range", "percent_fga_from_x16_3p_range", "percent_fga_from_x3p_range", "fg_percent_from_x2p_range", "fg_percent_from_x0_3_range", "fg_percent_from_x3_10_range", "fg_percent_from_x10_16_range", "fg_percent_from_x16_3p_range", "fg_percent_from_x3p_range", "percent_assisted_x2p_fg", "percent_assisted_x3p_fg", "percent_dunks_of_fga", "num_of_dunks", "percent_corner_3s_of_3pa", "corner_3_point_percent", "num_heaves_attempted", "num_heaves_made", "per", "x3p_ar", "f_tr", "orb_percent", "drb_percent", "trb_percent", "ast_percent", "stl_percent", "blk_percent", "tov_percent", "usg_percent", "ows", "dws", "ws", "ws_48", "obpm", "dbpm", "bpm", "vorp"]

    result = player_stats.groupby(['season','player_id']).apply(weighted_avg, weight_col='mp', stat_cols=player_metrics).reset_index()
    result['season'] = result['season'] + 1
    result.drop(columns=['mp'],inplace=True)
    result[(result['season'] == 2023) & (result['player_id'] == 5026)]

    player_stats_adjusted = player_stats.copy()
    player_stats_adjusted['full_season'] = player_stats_adjusted['season'].apply(lambda x: f"{x-1}-{str(x)[-2:]}")
    player_stats_adjusted = player_stats_adjusted[player_stats_adjusted['season'] != 1997]

    merged_df = pd.merge(player_stats_adjusted, result, on=['season', 'player_id'], suffixes=('', '_df2'), how='left')

    for field in player_metrics:
        merged_df[field] = merged_df[field + '_df2'].combine_first(merged_df[field])

    merged_df.drop(columns=[field + '_df2' for field in player_metrics], inplace=True)

    merged_df.to_csv('../data/interim/player_stats_year_adjusted.csv', index=False)

    df = pd.read_csv('../data/interim/player_stats_year_adjusted.csv')

    results = []
    position_columns = ['pos_PG', 'pos_SG', 'pos_PF', 'pos_SF', 'pos_C']
    stat_columns = player_metrics

    # Loop through each position
    for pos in position_columns:
        # Filter the DataFrame for players playing the current position
        df_pos = df[df[pos] == 1]
    
        # Group by team and season, and apply the weighted average function
        grouped = df_pos.groupby(['full_season', 'tm']).apply(weighted_avg_2, weight_col='mp', stat_cols=stat_columns).reset_index()
    
        # Add position prefix to the stat columns
        grouped = grouped.rename(columns={col: f'{pos}_{col}' for col in stat_columns})
    
        # Append the result to the results list
        results.append(grouped)
    
    # Start with the first result as the base DataFrame
    final_df = results[0]

    # Merge the rest of the results into the base DataFrame
    for df_pos in results[1:]:
        final_df = final_df.merge(df_pos, on=['full_season', 'tm'], how='outer')

    final_df = final_df.merge(team_stats, left_on=['full_season', 'tm'], right_on=['Season', 'Team'], how='left')
    final_df = final_df.dropna(subset=['W/L%'])
    final_df = final_df.dropna()

    final_df.to_csv('../data/interim/NBA_team_player_stats_Weight_Average.csv', index=False)

    return final_df

"""def agg_by_pos(player_df, team_df, save_file=False, use_pca=False, pca_model_path=None, output_dir=None):
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

    return df"""
