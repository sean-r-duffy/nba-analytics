import pandas as pd
from sklearn.neighbors import NearestNeighbors


def get_allstar_comps(player_list: list) -> list:
    """

    :param player_list:List of player names
    :return: List of all star player names
    """

    # Open All Star and Rookie Data
    all_stars_scaled = pd.read_csv('data/processed/all_stars_scaled.csv')
    rookies_scaled = pd.read_csv('data/processed/rookie_stats_scaled.csv', index_col="Player")

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
