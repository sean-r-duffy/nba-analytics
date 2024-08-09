import joblib
import json
import pandas as pd


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
    team_stats = team_stats[['Season', 'Team', 'W/L%']]
    columns_drop = ['Unnamed: 0','seas_id','g','gs','age','experience']
    player_stats = player_stats.drop(columns=columns_drop)

    player_metrics = ["fg_per_100_poss", "fga_per_100_poss", "x3p_per_100_poss", "x3pa_per_100_poss",
                      "x2p_per_100_poss", "x2pa_per_100_poss", "ft_per_100_poss", "fta_per_100_poss",
                      "orb_per_100_poss", "drb_per_100_poss", "trb_per_100_poss", "ast_per_100_poss",
                      "stl_per_100_poss", "blk_per_100_poss", "tov_per_100_poss", "pf_per_100_poss", "pts_per_100_poss",
                      "o_rtg", "d_rtg", "avg_dist_fga", "percent_fga_from_x2p_range", "percent_fga_from_x0_3_range",
                      "percent_fga_from_x3_10_range", "percent_fga_from_x10_16_range", "percent_fga_from_x16_3p_range",
                      "percent_fga_from_x3p_range", "fg_percent_from_x2p_range", "fg_percent_from_x0_3_range",
                      "fg_percent_from_x3_10_range", "fg_percent_from_x10_16_range", "fg_percent_from_x16_3p_range",
                      "fg_percent_from_x3p_range", "percent_assisted_x2p_fg", "percent_assisted_x3p_fg",
                      "percent_dunks_of_fga", "num_of_dunks", "percent_corner_3s_of_3pa", "corner_3_point_percent",
                      "num_heaves_attempted", "num_heaves_made", "per", "x3p_ar", "f_tr", "orb_percent", "drb_percent",
                      "trb_percent", "ast_percent", "stl_percent", "blk_percent", "tov_percent", "usg_percent", "ows",
                      "dws", "ws", "ws_48", "obpm", "dbpm", "bpm", "vorp"]

    result = player_stats.groupby(['season', 'player_id']).apply(weighted_avg, weight_col='mp',
                                                                 stat_cols=player_metrics).reset_index()
    result['season'] = result['season'] + 1
    result.drop(columns=['mp'], inplace=True)
    result[(result['season'] == 2023) & (result['player_id'] == 5026)]

    player_stats_adjusted = player_stats.copy()
    player_stats_adjusted['full_season'] = player_stats_adjusted['season'].apply(lambda x: f"{x - 1}-{str(x)[-2:]}")
    player_stats_adjusted = player_stats_adjusted[player_stats_adjusted['season'] != 1997]

    merged_df = pd.merge(player_stats_adjusted, result, on=['season', 'player_id'], suffixes=('', '_df2'), how='left')

    for field in player_metrics:
        merged_df[field] = merged_df[field + '_df2'].combine_first(merged_df[field])

    merged_df.drop(columns=[field + '_df2' for field in player_metrics], inplace=True)

    df = merged_df.copy()

    results = []
    position_columns = ['pos_PG', 'pos_SG', 'pos_PF', 'pos_SF', 'pos_C']
    stat_columns = player_metrics

    # Loop through each position
    for pos in position_columns:
        # Filter the DataFrame for players playing the current position
        df_pos = df[df[pos] == 1]

        # Group by team and season, and apply the weighted average function
        grouped = df_pos.groupby(['full_season', 'tm']).apply(weighted_avg_2, weight_col='mp',
                                                              stat_cols=stat_columns).reset_index()

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

    final_df.to_csv('../../data/processed/roster_stats.csv', index=False)

    return final_df


stat_columns = [
    'fg_per_100_poss', 'fga_per_100_poss', 'x3p_per_100_poss', 'x3pa_per_100_poss',
    'x2p_per_100_poss', 'x2pa_per_100_poss', 'ft_per_100_poss', 'fta_per_100_poss',
    'orb_per_100_poss', 'drb_per_100_poss', 'trb_per_100_poss', 'ast_per_100_poss',
    'stl_per_100_poss', 'blk_per_100_poss', 'tov_per_100_poss', 'pf_per_100_poss',
    'pts_per_100_poss', 'o_rtg', 'd_rtg', 'avg_dist_fga',
    'percent_fga_from_x2p_range', 'percent_fga_from_x0_3_range',
    'percent_fga_from_x3_10_range', 'percent_fga_from_x10_16_range',
    'percent_fga_from_x16_3p_range', 'percent_fga_from_x3p_range',
    'fg_percent_from_x2p_range', 'fg_percent_from_x0_3_range',
    'fg_percent_from_x3_10_range', 'fg_percent_from_x10_16_range',
    'fg_percent_from_x16_3p_range', 'fg_percent_from_x3p_range',
    'percent_assisted_x2p_fg', 'percent_assisted_x3p_fg',
    'percent_dunks_of_fga', 'num_of_dunks', 'percent_corner_3s_of_3pa',
    'corner_3_point_percent', 'num_heaves_attempted', 'num_heaves_made',
    'per', 'x3p_ar', 'f_tr', 'orb_percent', 'drb_percent', 'trb_percent',
    'ast_percent', 'stl_percent', 'blk_percent', 'tov_percent', 'usg_percent',
    'ows', 'dws', 'ws', 'ws_48', 'obpm', 'dbpm', 'bpm', 'vorp'
]
stat_columns_PG = ['pos_PG_' + stat for stat in stat_columns]
stat_columns_SG = ['pos_SG_' + stat for stat in stat_columns]
stat_columns_PF = ['pos_PF_' + stat for stat in stat_columns]
stat_columns_SF = ['pos_SF_' + stat for stat in stat_columns]
stat_columns_C = ['pos_C_' + stat for stat in stat_columns]


def create_potential_rosters(player_projections_df: pd.DataFrame, last_season_df: pd.DataFrame, team):
    df = pd.DataFrame()
    team_stats = last_season_df[last_season_df['tm'] == team]
    player_stats = player_projections_df.drop(columns=['g', 'gs', 'mp', 'height', 'weight'])

    for index, row in player_stats.iterrows():

        if row['pos_PG']:
            new_row = team_stats.iloc[0].copy()
            new_row['player'] = row['player']
            new_row[stat_columns_PG] = row[stat_columns]
            df = pd.concat([df, new_row.to_frame().T], ignore_index=True)

        if row['pos_SG']:
            new_row = team_stats.iloc[0].copy()
            new_row['player'] = row['player']
            new_row[stat_columns_SG] = row[stat_columns]
            df = pd.concat([df, new_row.to_frame().T], ignore_index=True)

        if row['pos_PF']:
            new_row = team_stats.iloc[0].copy()
            new_row['player'] = row['player']
            new_row[stat_columns_PF] = row[stat_columns]
            df = pd.concat([df, new_row.to_frame().T], ignore_index=True)

        if row['pos_SF']:
            new_row = team_stats.iloc[0].copy()
            new_row['player'] = row['player']
            new_row[stat_columns_SF] = row[stat_columns]
            df = pd.concat([df, new_row.to_frame().T], ignore_index=True)

        if row['pos_C']:
            new_row = team_stats.iloc[0].copy()
            new_row['player'] = row['player']
            new_row[stat_columns_C] = row[stat_columns]
            df = pd.concat([df, new_row.to_frame().T], ignore_index=True)

    return df


def predict_win_percentages(potential_rosters_df: pd.DataFrame, model_path):
    df = potential_rosters_df.drop(columns=['full_season', 'tm', 'Season'])
    model = joblib.load(model_path)
    win_pred = model.predict(df.drop(columns=['player']))
    df['win%'] = win_pred

    return df[['player', 'win%']]


def calculate_top_players_ui(selected_team: str, available_players: list) -> dict:

    # Team Mappings
    with open('data/processed/team_abbr_mapping.json', 'r') as file:
        mappings = json.load(file)
    team = mappings[selected_team]

    # Loading dataframes
    projections_df = pd.read_csv('data/processed/rookie_projection_stats.csv')
    last_season_df = pd.read_csv('data/processed/roster_stats_2024.csv')

    # Filtering for available players
    projections_df = projections_df[projections_df['player'].isin(available_players)]

    # Make predictions
    potential_rosters_df = create_potential_rosters(projections_df, last_season_df, team)
    predictions = predict_win_percentages(potential_rosters_df, 'models/win_prediction.pkl')

    # Convert to dictionary
    predictions = predictions.groupby(by='player').max().sort_values('win%', ascending=False).reset_index().head(10)
    predictions = predictions.to_dict()

    return predictions


def fit_model():
    # TODO: Scale features to get better feature importance
    pass
