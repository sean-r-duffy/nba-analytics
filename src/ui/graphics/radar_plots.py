import matplotlib.pyplot as plt
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from math import pi

def make_radar_plot(name):
    with open("data/processed/rookie_stats.csv", 'r') as f1:
        df = pd.read_csv(f1, index_col="Player")
    df = df.drop(["Pos"], axis=1)
    df["REB"] = df["ORB"] + df ["DRB"]
    features = [ 'PTS', '3P', 'REB', 'AST', 'STL', 'BLK','FG%']
    df = df[features]
    scaler = MinMaxScaler()
    df_scaled = scaler.fit_transform(df)
    df_scaled = pd.DataFrame(df_scaled, columns=features)
    df_scaled.index = df.index
    categories = list(df_scaled.columns)
    N = len(categories)
    values = df_scaled.loc[name].values.flatten().tolist()
    values += values[:1]
    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += angles[:1]
    ax = plt.subplot(111, polar=True)
    plt.xticks(angles[:-1], categories, color='grey', size=8)
    ax.set_rlabel_position(0)
    plt.yticks([10,20,30], ["10","20","30"], color="grey", size=7)
    plt.ylim(0,1)
    ax.plot(angles, values, linewidth=1, linestyle='solid')
    ax.fill(angles, values, 'b', alpha=0.1)
    return ax.figure