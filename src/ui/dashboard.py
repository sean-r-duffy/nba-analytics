import streamlit as st
import pandas as pd
from src.models.nn_search import get_allstar_comps

print(st.session_state)
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
st.session_state.rookie_names = list(rookie_stats.index)
st.session_state.df = rookie_stats


def calculate_top_players(selected_team: str) -> dict:
    # fill with model
    return {"Player": ["Baylor Scheierman", "Donovan Clingan", "Zach Edey", "Kyle Filipowski"],
            "Win%": [.89, .78, .67, .45]}


@st.fragment
def update_model():
    team = st.selectbox("Select your Team", teams, key=42)
    if (st.button('Enter')):
        st.subheader(f"Best Available for your the {team}")
        top_players = pd.DataFrame(calculate_top_players(team))
        player_comparisons = get_allstar_comps(list(top_players["Player"]))
        top_players["All Star Comparison"] = player_comparisons
        st.dataframe(top_players, hide_index=True)


@st.fragment
def display_stats():
    st.subheader("Available Players")

    drafted = st.selectbox("Select Drafted Player", st.session_state.rookie_names, key=15)
    if st.session_state.i <= 1:
        print(6)
        st.session_state.i += 1
    if (st.button('Remove Drafted Player')):
        if st.session_state.i > 1:
            print(5)
            st.session_state.df = st.session_state.df.drop(drafted)
            updated_names = list(st.session_state.rookie_names)
            updated_names.remove(drafted)
            st.session_state.rookie_names = updated_names
    st.dataframe(st.session_state.df)


st.header("NBA Draft Companion")
update_model()
display_stats()