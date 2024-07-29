import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors


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


def get_allstar_comps(player_list: list) -> list:
    # Open All Star and Rookie Data
    with open('../../data/processed/all_stars_scaled.csv', 'r') as f1:
        # cant use player name as index since there are mulitples for player seasons
        all_stars_scaled = pd.read_csv(f1)
    with open('../../data/processed/rookie_stats_scaled.csv', 'r') as f2:
        rookies_scaled = pd.read_csv(f2, index_col="Player")
    # Fit KNN Model
    knn = NearestNeighbors(n_neighbors=1)
    all_stars_scaled_n = all_stars_scaled.iloc[:, 1:]
    knn.fit(all_stars_scaled_n.values)
    # Run KNN on All Rookie Suggestions
    player_comps = []
    for rookie in player_list:
        player_data = rookies_scaled.loc[rookie].to_numpy().reshape(1, -1)
        dists, idxs = knn.kneighbors(player_data)
        idxs = idxs[0].tolist()
        i = idxs[0]
        as_name = list(all_stars_scaled["Player"])[i]
        player_comps.append(as_name)
    return player_comps
