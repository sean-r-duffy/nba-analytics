import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors


def combine_search(player_idx, n=5, impute='mean', all_nba=False):
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