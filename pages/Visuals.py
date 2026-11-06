# This creates the page for displaying data visualizations.

import json
from pathlib import Path

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Visuals",
    page_icon="📈",
)

# PAGE TITLE
st.title("Data Visualizations 📈")


# PART 1: GRAPHS FROM data.json
here = Path(__file__).resolve().parent
json_path = here / "data.json"
if not json_path.exists():
    json_path = here.parent / "data.json"

with open(json_path) as infile:
    myData = json.load(infile)

df = pd.DataFrame(myData["data_points"])
df = df.rename(columns={"label": "Player", "value": "Goals"})

st.header(myData["chart_title"])

# --- Static chart: Matplotlib bar chart ---
st.subheader("Goals by Player")

sorted_df = df.sort_values("Goals", ascending=False)

fig, ax = plt.subplots()
ax.bar(sorted_df["Player"], sorted_df["Goals"], color="#034694")
ax.set_title("Goals Scored by Each Chelsea Player")
ax.set_xlabel("Player")
ax.set_ylabel("Goals")
plt.xticks(rotation=30, ha="right")
st.pyplot(fig)

top = sorted_df.iloc[0]
st.write(f"**{top['Player']}** leads Chelsea with **{top['Goals']}** goals.")

# --- Dynamic chart: Plotly pie chart with session state ---
st.subheader("Share of Chelsea's Goals (Interactive)")

if "min_goals" not in st.session_state:
    st.session_state["min_goals"] = 1
if "donut" not in st.session_state:
    st.session_state["donut"] = False

st.slider(
    "Show only players with at least this many goals",
    0, max(1, int(df["Goals"].max())),
    key="min_goals",
)
st.checkbox("Show as donut", key="donut")

filtered = df[df["Goals"] >= st.session_state["min_goals"]]
filtered = filtered[filtered["Goals"] > 0]

if filtered.empty:
    st.warning("No players match. Lower the slider or add goals to data.json.")
else:
    fig2 = px.pie(
        filtered,
        names="Player",
        values="Goals",
        hole=0.4 if st.session_state["donut"] else 0,
        title="Each Player's Share of Their Goals",
    )
    st.plotly_chart(fig2)
    st.write(f"{len(filtered)} players shown, with {filtered['Goals'].sum()} goals combined.")


# PART 2: GRAPHS FROM data.csv
def find_csv():
    here = Path(__file__).resolve().parent
    for p in (here / "data.csv", here.parent / "data.csv"):
        if p.exists():
            return p
    return None

csv_path = find_csv()
if csv_path is None:
    st.warning("data.csv not found. Take the survey first.")
else:
    survey_df = pd.read_csv(csv_path).iloc[:, :2]
    survey_df.columns = ["category", "value"]
    survey_df["value"] = pd.to_numeric(survey_df["value"], errors="coerce")
    survey_df = survey_df.dropna()

    st.header("Chelsea Fan Survey Results")

    if survey_df.empty:
        st.warning("No survey responses yet. Take the survey on the Survey page.")
    else:
        st.write(f"{len(survey_df)} responses collected.")

        # --- Static chart: Matplotlib bar chart ---
        st.subheader("Average Matches Watched by Favorite Player (Static)")

        avg = survey_df.groupby("category")["value"].mean().sort_values(ascending=False)

        fig3, ax3 = plt.subplots()
        ax3.bar(avg.index, avg.values, color="#034694")
        ax3.set_title("Average Matches Watched Per Month by Favorite Player")
        ax3.set_xlabel("Favorite Player")
        ax3.set_ylabel("Average Matches Per Month")
        plt.xticks(rotation=30, ha="right")
        st.pyplot(fig3)

        st.write(f"Fans of **{avg.index[0]}** watch the most, at {avg.iloc[0]:.1f} matches a month on average.")

        # --- Dynamic chart: Plotly histogram with session state ---
        st.subheader("Distribution of Matches Watched (Interactive)")

        all_players = sorted(survey_df["category"].unique())

        if "survey_players" not in st.session_state:
            st.session_state["survey_players"] = all_players
        if "bins" not in st.session_state:
            st.session_state["bins"] = 5

        st.multiselect("Favorite players to include", all_players, key="survey_players")
        st.slider("Number of bins", 2, 15, key="bins")

        view = survey_df[survey_df["category"].isin(st.session_state["survey_players"])]

        if view.empty:
            st.warning("Pick at least one player.")
        else:
            fig4 = px.histogram(
                view, x="value", color="category", nbins=st.session_state["bins"],
                title="How Many Matches Do Fans Watch Per Month?",
                labels={"value": "Matches Watched Per Month", "category": "Favorite Player"},
            )
            fig4.update_layout(yaxis_title="Number of Fans")
            st.plotly_chart(fig4)
            st.write(f"Showing {len(view)} responses. Average: {view['value'].mean():.1f} matches a month.")
