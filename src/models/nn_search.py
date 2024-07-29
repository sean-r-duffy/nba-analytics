import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors

# TODO Fix paths
# TODO Change so that players in same draft class will not be returned
def combine_search(player_idx, n=5, impute='knn', all_nba=False):
    assert impute == 'mean' or impute == 'knn'

    combine_df = pd.read_csv('../data/interim/combine_stats_trimmed.csv')

    if all_nba:
        df_all_nba = pd.read_csv('../data/all_nba_expanded.csv')
        all_nba_players = set(df_all_nba['Player Name'])
        combine_df = combine_df[(combine_df['player'].isin(all_nba_players)) | (combine_df['year'] == '2024-25')]

    num_df = combine_df.select_dtypes(include=['number'])
    num_cols = num_df.columns.tolist()

    if impute == 'mean':
        column_means = combine_df[num_cols].mean()
        combine_df[num_cols] = combine_df[num_cols].fillna(column_means)
    else:
        imputer = KNNImputer(n_neighbors=5)
        combine_df[num_cols] = imputer.fit_transform(combine_df[num_cols])

    scaler = StandardScaler()
    combine_df[num_cols] = scaler.fit_transform(combine_df[num_cols])

    knn = NearestNeighbors(n_neighbors=n + 1)
    knn.fit(combine_df[num_cols])

    distances, indices = knn.kneighbors([combine_df.iloc[player_idx][num_cols]])

    return combine_df.iloc[indices.tolist()[0]]


# TODO Fix: Returning NaN when players can't be found
def get_nba_projection(players, years):
    combine_df = pd.read_csv('../data/interim/combine_stats_trimmed.csv')

    df = pd.DataFrame()

    for player in players:
        similar_players = combine_search(player)
        similar_players = similar_players['player'].tolist()[1:]

        player_name = combine_df.iloc[player]['player']
        player_position = combine_df.iloc[player]['pos']
        player_height = combine_df.iloc[player]['height_wo_shoes']
        player_weight = combine_df.iloc[player]['weight_lbs']

        stats_df = pd.read_csv('../data/processed/player_data_clean.csv')
        stats_df = stats_df[stats_df['player'].isin(similar_players)]
        stats_df = stats_df[stats_df['experience'] == years]
        stats_df = stats_df.drop(
            columns=['Unnamed: 0', 'seas_id', 'season', 'player_id', 'player', 'age', 'tm', 'g', 'gs', 'mp',
                     'pos_PG', 'pos_SG', 'pos_PF', 'pos_SF', 'pos_C'])
        stats_df = pd.DataFrame(stats_df.mean()).transpose()
        stats_df['height'] = player_height
        stats_df['weight'] = player_weight
        stats_df['player'] = player_name
        stats_df['pos'] = player_position

        df = pd.concat([df, stats_df])

    return df
