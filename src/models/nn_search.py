import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors


# TODO Fix: Returning NaN when players can't be found
def get_nba_projection(players, years):
    pass


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
