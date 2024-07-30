import streamlit as st
import pandas as pd
import sys
sys.path.append('../../../nba-analytics')
from src.models.nn_search import get_allstar_comps
from src.models.win_prediction import calculate_top_players_ui
from src.ui.graphics.radar_plots import make_radar_plot


print("app start")
st.session_state.i = 1

# All NBA Teams
teams = ["Atlanta Hawks", "Boston Celtics", "Brooklyn Nets", "Charlotte Hornets", "Chicago Bulls",
         "Cleveland Cavaliers",
         "Dallas Mavericks", "Denver Nuggets", "Detroit Pistons", "Golden State Warriors", "Houston Rockets",
         "Indiana Pacers",
         "Los Angeles Clippers", "Los Angeles Lakers", "Memphis Grizzlies", "Miami Heat", "Milwaukee Bucks",
         "Minnesota Timberwolves",
         "New Orleans Pelicans", "New York Knicks", "Oklahoma City Thunder", "Orlando Magic", "Philadelphia 76ers",
         "Phoenix Suns",
         "Portland Trail Blazers", "Sacramento Kings", "San Antonio Spurs", "Toronto Raptors", "Utah Jazz",
         "Washington Wizards"]

# Load Rookie Stats for Display
rookie_stats = pd.read_csv("../../data/processed/rookie_stats_raw.csv", index_col="Player")
rookie_names = list(rookie_stats.index)
st.session_state.all_rookie_names = rookie_names
st.session_state.rookie_names = rookie_names
st.session_state.rookies_df = rookie_stats


@st.experimental_fragment
def update_model():
    team = st.selectbox("Select your Team", teams, key=42)
    if st.button('Enter'):
        print(f"update table for {team}")
        st.subheader(f"Best Available Players for the {team}")
        available_rookies = list(st.session_state.rookies_df.index)
        top_players = pd.DataFrame(calculate_top_players_ui(team, available_rookies))
        player_comparisons = get_allstar_comps(list(top_players["Player"]))
        top_players["All Star Comparison"] = player_comparisons
        st.dataframe(top_players, hide_index=True)


@st.experimental_fragment
def display_stats():
    st.subheader("Available Players")
    drafted = st.selectbox("Select Drafted Player", st.session_state.rookie_names, key=15)
    if st.session_state.i <= 1:
        st.session_state.i += 1
    if st.button('Remove Drafted Player'):
        if st.session_state.i > 1:
            st.session_state.rookies_df = st.session_state.rookies_df.drop(drafted)
            updated_names = list(st.session_state.rookie_names)
            updated_names.remove(drafted)
            st.session_state.rookie_names = updated_names
    st.dataframe(st.session_state.rookies_df)

@st.experimental_fragment
def display_plot():
    st.subheader("Player Radar Plot")
    player_plot = st.selectbox("Select Player", st.session_state.all_rookie_names, key=25)
    if st.button("Plot Stats"):
        ca, c2, c3 = st.columns([1,2,1])
        with c2:
            st.pyplot(make_radar_plot(player_plot))

st.logo("https://cdn.freebiesupply.com/images/large/2x/nba-logo-transparent.png", link="https://www.nba.com")
st.image("https://on3static.com/uploads/dev/assets/cms/2024/03/12155413/NBADraft-AFI-1.png")
st.header("NBA Draft Companion")
update_model()
display_stats()
display_plot()