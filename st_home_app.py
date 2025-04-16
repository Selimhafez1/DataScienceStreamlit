
import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt
import pickle

# Helper function to load .pkl figure files
def load_figure(path):
    with open(path, "rb") as f:
        return pickle.load(f)

# Load trained model (pipeline)
model = joblib.load("home_advantage_model.pkl")

# Load dataset to populate dropdowns
df = pd.read_csv("Final_Home_Advantage.csv")
df = df[['Season', 'HomeTeam', 'AwayTeam']].dropna()

seasons = sorted(df['Season'].unique())
home_teams = sorted(df['HomeTeam'].unique())
away_teams = sorted(df['AwayTeam'].unique())

# Load saved charts
home_advantage_barchart = load_figure("home_advantage_barchart.pkl")
home_advantage_linechart = load_figure("home_advantage_linechart.pkl")
height_barchart = load_figure("height_barchart.pkl")
height_positions_boxplot = load_figure("height_positions_boxplot.pkl")
age_injuries_avg = load_figure("age_injury_avg.pkl")
age_injuries_scatter = load_figure("age_injuries_scatter.pkl")

# App Title
st.title("⚽ Football Match Outcome Predictor")

# -------------------------
# SECTION: Visualizations (with Tabs)
# -------------------------
st.subheader("📊 Data Visualizations")

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "Home vs Away Bar Chart",
    "Home vs Away Line Chart",
    "Height vs Position Bar Chart",
    "Height Distribution by Position Box Plot",
    "Age vs Injuries Bar Chart",
    "Age vs Injuries Scatter Plot"
])

with tab1:
    st.pyplot(home_advantage_barchart)
    st.markdown("""
    * Home teams have won around **21,000** games from the games in the dataset.  
    * Away teams have won around **12,500** games from the games in the dataset.  
    * Draws have occurred around **11,500** times amongst both the home and away teams.  
    * Home teams have almost **double the possibility** of winning compared to away teams.
    """)

with tab2:
    st.pyplot(home_advantage_linechart)
    st.markdown("""
    * The gap between home and away teams average goals per team is **decreasing** over time.
    * The season which had no fans (due to covid), the home teams **barely** scored more goals than away teams. This shows the **importance of fans** in the home stadiums.
    * Home teams are **consistently** scoring more goals in general more than away teams.
    """)

with tab3:
    st.pyplot(height_barchart)
    st.markdown("""
    * Goalkeepers have an average height of around **190** cm which means they're the **tallest** position amongst all other positions.
    * Defenders have an average height of around **184** cm which makes them still tall, but maybe they do not require height as much as goalkeepers.
    * Midfielders have the **shortest** average height which makes them the position which maybe doesn't require height.
    * Forwards have an average height of around **181** cm which means that they're a position which has an average range when it comes to height in that position.
    """)

with tab4:
    st.pyplot(height_positions_boxplot)
    st.markdown("""
    * Goalkeepers are the **tallest** players on average with the **highest** median.
    * Defenders are also tall, and have a **wide** range (maybe fullbacks are shorter).
    * **Both** forwards and midfielders are short, but midfielders are the **shortest** position.
    * **All** groups have outliers, but goalkeepers are more **consistent** when it comes to height.
    """)

with tab5:
    st.pyplot(age_injuries_avg)
    st.markdown("""
    * There's **no** strict trend indicating a relationship between age and injury duration. 
    * Players of ages **17, 35, 38, and 39** have **high** averages. However, this could be due to how **small** the count of players in these ages are. 
    * A takeaway could be that ages at **extreme ends** of their career whether that's the beginning or end, are **more prone** to long term injuries.
    """)

with tab6:
    st.pyplot(age_injuries_scatter)
    st.markdown("""
    * Curve is **almost** flat, but **very** tiny slope upwards after the age of 30.
    * Injury duration doesn't change **noticably** with age (**very** small increase as they get older).
    * **Weak**-positive correlation.
    """)


# -------------------------
# SECTION: Predictor
# -------------------------
st.subheader("🔮 Predict Match Outcome")

col1, col2 = st.columns(2)

with col1:
    season = st.selectbox("Season", seasons)

with col2:
    home_team = st.selectbox("Home Team", home_teams)
    away_team = st.selectbox("Away Team", away_teams)

if st.button("Predict Result"):
    input_df = pd.DataFrame([[season, home_team, away_team]],
                            columns=["Season", "HomeTeam", "AwayTeam"])

    prediction = model.predict(input_df)[0]
    probabilities = model.predict_proba(input_df)[0]

    st.subheader("Prediction Result")
    st.write(f"**Predicted Match Outcome:** {prediction}")

    st.write("**Prediction Probabilities:**")
    st.write(f"- Home Win (H): {probabilities[model.classes_.tolist().index('H')]:.2%}")
    st.write(f"- Draw (D): {probabilities[model.classes_.tolist().index('D')]:.2%}")
    st.write(f"- Away Win (A): {probabilities[model.classes_.tolist().index('A')]:.2%}")
