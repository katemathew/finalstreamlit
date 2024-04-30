import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

# Function to load data
def load_setlist_data():
    return pd.read_csv('setlist_data.csv')

def load_filtered_spotify_data():
    return pd.read_csv('filtered_spotify_data.csv')

def load_spotify_tracks_db():
    engine = create_engine('sqlite:///spotify_tracks.db')
    with engine.connect() as conn:
        tracks = pd.read_sql_table('tracks', conn)
        albums = pd.read_sql_table('albums', conn)
        artists = pd.read_sql_table('artists', conn)
    return tracks, albums, artists

# Function to analyze overlaps
def analyze_overlaps(df1, df2, key='Artist'):
    return pd.merge(df1, df2, on=key, how='inner')

# Visualizing data
def plot_data(df):
    fig, ax = plt.subplots()
    # Example plot: popularity distribution
    df['popularity'].hist(ax=ax)
    st.pyplot(fig)

# Layout
st.title('Music Data Analysis App')

# Load data
setlist_data = load_setlist_data()
spotify_data = load_filtered_spotify_data()
tracks, albums, artists = load_spotify_tracks_db()

# Display data
st.header('Setlist Data')
st.write(setlist_data.head())

st.header('Spotify Filtered Data')
st.write(spotify_data.head())

st.header('Spotify Tracks Data')
st.write(tracks.head())

# Overlaps
st.header('Overlaps in Artists')
overlaps = analyze_overlaps(setlist_data, spotify_data, 'Artist')
st.write(overlaps)

# Visualization
st.header('Song Popularity Analysis')
plot_data(tracks)
