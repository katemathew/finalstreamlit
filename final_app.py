import os
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from sqlalchemy import create_engine, Column, String, Integer, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from dotenv import load_dotenv
import logging
import spotipy
import seaborn as sns
from spotipy.oauth2 import SpotifyClientCredentials

# Load environment variables from .env file
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)

# Database schema setup
Base = declarative_base()

class Artist(Base):
    __tablename__ = 'artists'
    id = Column(String, primary_key=True)
    name = Column(String)
    albums = relationship("Album", back_populates="artist")

class Album(Base):
    __tablename__ = 'albums'
    id = Column(String, primary_key=True)
    name = Column(String)
    release_date = Column(String)
    artist_id = Column(String, ForeignKey('artists.id'))
    artist = relationship("Artist", back_populates="albums")
    tracks = relationship("Track", back_populates="album")

class Track(Base):
    __tablename__ = 'tracks'
    id = Column(String, primary_key=True)
    name = Column(String)
    popularity = Column(Integer)
    duration_ms = Column(Integer)
    album_id = Column(String, ForeignKey('albums.id'))
    album = relationship("Album", back_populates="tracks")

# Initialize Spotify client
client_id = '5b2023b50cd44ccca291f436252f1381'
client_secret = 'b87bc93755134e1e97bf139ca8855ca7'
credentials = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=credentials)

def fetch_artist_top_tracks(artist_uri):
    results = sp.artist_top_tracks(artist_uri)
    tracks_data = []
    for track in results['tracks']:
        track_data = {
            'track_id': track['id'],
            'name': track['name'],
            'popularity': track['popularity'],
            'duration_ms': track['duration_ms'],
            'album_id': track['album']['id'],
            'album_name': track['album']['name'],
            'release_date': track['album']['release_date'],
            'artist_id': track['artists'][0]['id'],
            'artist_name': track['artists'][0]['name']
        }
        tracks_data.append(track_data)
    return tracks_data

def clean_artist_name(name):
    """Clean artist names by removing unwanted characters and making them lowercase."""
    return name.replace('[', '').replace(']', '').replace("'", "").strip().lower()

def display_trends(df):
    if df.empty:
        st.write("No data available for analysis.")
        return
    
    # Initialize a dictionary to store the names and average values of the metrics
    metrics = {
        'danceability': 'Danceability',
        'energy': 'Energy',
        'instrumentalness': 'Instrumentalness',
        'liveness': 'Liveness',
        'loudness': 'Loudness',
        'speechiness': 'Speechiness',
        'tempo': 'Tempo',
        'valence': 'Valence'
    }

    # Loop through the dictionary, calculate the mean, and display results
    for metric, display_name in metrics.items():
        if metric in df.columns:
            average_value = df[metric].mean()
            st.write(f"**Average {display_name}:** {average_value:.2f}")
        else:
            st.write(f"{display_name} data not available.")



def fetch_and_save_spotify_data():
    artist_uris = {
        'Morgan Wallen': 'spotify:artist:4oUHIQIBe0LHzYfvXNW4QM',
        'Taylor Swift': 'spotify:artist:06HL4z0CvFAxyc27GXpf02',
        'Bad Bunny': 'spotify:artist:4q3ewBCX7sLwd24euuV69X',
        'The Weeknd': 'spotify:artist:1Xyo4u8uXC1ZmMpatF05PJ',
        'Drake': 'spotify:artist:3TVXtAsR1Inumwj472S9r4',
        'Peso Pluma': 'spotify:artist:12GqGscKJx3aE4t07u7eVZ',
        'Tame Impala': 'spotify:artist:5INjqkS1o8h1imAzPqGZBb'
    }

    database_url = "postgresql://u4ja2bod19v7gd:p9e70065bd97ea89a78fd91429d857f1c6dcb32c248a847c624d3a359bdeba876@ce1r1ldap2qd4b.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/db3gjtci88doqv"

    # Database connection setup
    engine = create_engine(database_url)
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        for artist_name, artist_uri in artist_uris.items():
            try:
                tracks_data = fetch_artist_top_tracks(artist_uri)
                for data in tracks_data:
                    try:
                        artist = session.query(Artist).filter_by(id=data['artist_id']).first()
                        if not artist:
                            artist = Artist(id=data['artist_id'], name=data['artist_name'])
                            session.add(artist)
                        album = session.query(Album).filter_by(id=data['album_id']).first()
                        if not album:
                            album = Album(id=data['album_id'], name=data['album_name'], release_date=data['release_date'], artist=artist)
                            session.add(album)
                        track = session.query(Track).filter_by(id=data['track_id']).first()
                        if not track:
                            track = Track(id=data['track_id'], name=data['name'], popularity=data['popularity'], duration_ms=data['duration_ms'], album=album)
                            session.add(track)
                    except Exception as e:
                        logging.error(f"Error saving track data for {artist_name}: {e}")
            except Exception as e:
                logging.error(f"Error fetching Spotify data for {artist_name}: {e}")
            session.commit()
    except Exception as e:
        logging.error(f"Database operation failed: {e}")
        session.rollback()
    finally:
        session.close()
    # try:
    #     for artist_name, artist_uri in artist_uris.items():
    #         tracks_data = fetch_artist_top_tracks(artist_uri)
    #         for data in tracks_data:
    #             artist = session.query(Artist).filter_by(id=data['artist_id']).first()
    #             if not artist:
    #                 artist = Artist(id=data['artist_id'], name=data['artist_name'])
    #                 session.add(artist)
    #             album = session.query(Album).filter_by(id=data['album_id']).first()
    #             if not album:
    #                 album = Album(id=data['album_id'], name=data['album_name'], release_date=data['release_date'], artist=artist)
    #                 session.add(album)
    #             track = session.query(Track).filter_by(id=data['track_id']).first()
    #             if not track:
    #                 track = Track(id=data['track_id'], name=data['name'], popularity=data['popularity'], duration_ms=data['duration_ms'], album=album)
    #                 session.add(track)
    #         session.commit()
    #         logging.info(f"Data for {artist_name} successfully saved to the database")
    # except Exception as e:
    #     logging.error(f"An error occurred: {e}")
    #     session.rollback()
    # finally:
    #     session.close()



# Remaining functions remain unchanged


# def load_setlist_data():
#     df = pd.read_csv('setlist_data.csv')
#     df.rename(columns={'Artist Name': 'Artist'}, inplace=True)
#     return df

# def load_filtered_spotify_data():
#     df = pd.read_csv('filtered_spotify_data.csv')
#     # Removing brackets and quotes from artist names
#     df['Artist'] = df['artists'].str.replace(r"[\[\]']", "", regex=True)
#     return df

def load_setlist_data():
    df = pd.read_csv('setlist_data.csv')
    # Ensure the column 'Artist' exists. If the column name is different, adjust it here.
    df['Artist'] = df['Artist'].apply(clean_artist_name)
    return df

def load_filtered_spotify_data():
    df = pd.read_csv('filtered_spotify_data.csv')
    df['Artist'] = df['artists'].apply(clean_artist_name)
    return df

def load_spotify_tracks_db():
    database_url = "postgresql://u4ja2bod19v7gd:p9e70065bd97ea89a78fd91429d857f1c6dcb32c248a847c624d3a359bdeba876@ce1r1ldap2qd4b.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/db3gjtci88doqv"

    # Database connection setup
    engine = create_engine(database_url)
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        # Using select_from to explicitly start from Track and join to Album and Artist
        tracks = pd.read_sql(
            session.query(
                Track.id.label('track_id'),
                Track.name.label('name'),
                Track.popularity,
                Track.duration_ms,
                Album.name.label('Album'),
                Artist.name.label('Artist')
            )
            .select_from(Track)
            .join(Album, Track.album_id == Album.id)
            .join(Artist, Album.artist_id == Artist.id)
            .statement, 
            engine
        )
        tracks['Artist'] = tracks['Artist'].apply(clean_artist_name)
    finally:
        session.close()

    return tracks

# def analyze_overlaps(df1, df2, key='Artist'):
#     return pd.merge(df1, df2, on=key, how='inner')

# def analyze_overlaps(df1, df2, key='Artist'):
#     common = pd.merge(df1, df2, on=key, how='inner')
#     return common

# combined_data = analyze_overlaps(setlist_data, spotify_data, tracks, 'Artist')

def analyze_overlaps(df1, df2, df3, key='Artist'):
    combined_data = pd.merge(df1, df2, on=key, how='inner')
    final_combined_data = pd.merge(combined_data, df3, on=key, how='inner')
    return final_combined_data

# def plot_data(df):
#     if df.empty:
#         st.write("No data available to plot.")
#         return

#     # Adding a slider to control the number of bins in the histogram
#     bins = st.slider("Select number of bins for histogram:", min_value=10, max_value=100, value=20, step=5)
    
#     fig, ax = plt.subplots()
#     df['popularity'].hist(ax=ax, bins=bins)
#     ax.set_xlabel('Popularity')
#     ax.set_ylabel('Frequency')
#     st.pyplot(fig)

def plot_data(df):
    if df.empty:
        st.write("No data available to plot.")
        return

    # Histogram for Popularity
    if 'popularity' in df.columns:
        bins = st.slider("Select number of bins for histogram:", min_value=10, max_value=100, value=20, step=5)
        fig, ax = plt.subplots()
        df['popularity'].hist(ax=ax, bins=bins)
        ax.set_xlabel('Popularity')
        ax.set_ylabel('Frequency')
        st.pyplot(fig)

    # Line plot for album release date trends
    if 'release_date' in df.columns and not df['release_date'].isnull().all():
        df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')
        df = df.dropna(subset=['release_date'])  # Ensure no null values
        df['release_year'] = df['release_date'].dt.year
        release_trends = df.groupby('release_year').size()

        if not release_trends.empty:
            fig, ax = plt.subplots()
            release_trends.plot(kind='line', ax=ax)
            ax.set_title('Album Release Trends')
            ax.set_xlabel('Year')
            ax.set_ylabel('Number of Albums Released')
            st.pyplot(fig)
        else:
            st.write("No sufficient data for release trends.")

def plot_alternative_visualizations(df):
    if df.empty:
        st.write("No data available to plot.")
        return

    # # Bar Chart for Album Releases by Year
    # if 'release_date' in df.columns:
    #     # Debugging: Output original data sample
    #     st.write("Original date samples:", df['release_date'].head())

    #     # Explicitly specify the date format for parsing
    #     df['release_date'] = pd.to_datetime(df['release_date'], format='%m/%d/%y', errors='coerce')

    #     # Debugging: Check if dates are parsed correctly
    #     st.write("Parsed dates:", df['release_date'].

    # Box Plot for Track Popularity
    if 'popularity' in df.columns:
        fig, ax = plt.subplots()
        df['popularity'].plot(kind='box', ax=ax)
        ax.set_title('Popularity Distribution')
        ax.set_ylabel('Popularity Score')
        st.pyplot(fig)

    # Scatter Plot for Popularity vs. Track Duration
    if 'popularity' in df.columns and 'duration_ms' in df.columns:
        # Convert duration from milliseconds to seconds
        df['duration_sec'] = df['duration_ms'] / 1000

        fig, ax = plt.subplots()
        df.plot(kind='scatter', x='duration_sec', y='popularity', ax=ax)
        ax.set_title('Popularity vs. Track Duration')
        ax.set_xlabel('Duration (seconds)')
        ax.set_ylabel('Popularity')
        st.pyplot(fig)

def additional_visualizations(df):
    if df.empty:
        st.write("No data available for plot.")
        return

    # Time Series Plot for Popularity Over Time
    if 'release_date' in df.columns and 'popularity' in df.columns:
        df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')
        time_data = df.dropna(subset=['release_date', 'popularity'])
        time_data = time_data.sort_values('release_date')
        fig, ax = plt.subplots()
        sns.lineplot(x='release_date', y='popularity', data=time_data, ax=ax)
        ax.set_title('Popularity Over Time')
        ax.set_xlabel('Release Date')
        ax.set_ylabel('Popularity')
        st.pyplot(fig)

    # Correlation Heatmap
    if set(['popularity', 'duration_ms']).issubset(df.columns):
        # You might need to scale or adjust these columns
        correlation_data = df[['popularity', 'duration_ms']]
        correlation = correlation_data.corr()
        fig, ax = plt.subplots()
        sns.heatmap(correlation, annot=True, cmap='coolwarm', ax=ax)
        ax.set_title('Correlation Heatmap')
        st.pyplot(fig)

    # Pie Chart for Album Contribution
    if 'Album' in df.columns and 'popularity' in df.columns:
        album_contribution = df.groupby('Album')['popularity'].sum()
        fig, ax = plt.subplots()
        album_contribution.plot(kind='pie', ax=ax, autopct='%1.1f%%')
        ax.set_title('Album Contribution to Overall Popularity')
        ax.set_ylabel('')
        st.pyplot(fig)
        
def main():
    st.title('Music Data Analysis App')
    setlist_data = load_setlist_data()
    spotify_data = load_filtered_spotify_data()
    tracks = load_spotify_tracks_db()
    st.header('Setlist Data')
    st.write(setlist_data.head())
    st.header('Spotify Filtered Data')
    st.write(spotify_data.head())
    st.header('Spotify Tracks Data')
    st.write(tracks.head()) 


    # Artist selection dropdown
    artist_list = tracks['Artist'].unique()
    selected_artist = st.selectbox('Select an Artist', artist_list)

    # Filter data by selected artist
    filtered_setlist_data = setlist_data[setlist_data['Artist'] == selected_artist]
    filtered_spotify_data = spotify_data[spotify_data['Artist'] == selected_artist]
    filtered_tracks = tracks[tracks['Artist'] == selected_artist]

    # Display Combined Data for selected artist
    st.header(f'Combined Data for {selected_artist}')
    combined_data = analyze_overlaps(filtered_setlist_data, filtered_spotify_data, filtered_tracks, 'Artist')
    st.write(combined_data)

    st.header('Song Popularity')
    plot_data(filtered_tracks)

     # Explanation about Spotify Popularity Index
    st.header(f'Visualizations for {selected_artist}')
    st.markdown("""
    **The Spotify Popularity Index** is a 0-to-100 score that ranks how popular an artist is relative to other artists on Spotify. As your numbers grow, you'll get placed in more editorial playlists and increase your reach on algorithmic playlists and recommendations.
    """)

    plot_alternative_visualizations(filtered_tracks)

    # New Section for Advanced Visualizations
    st.header('Advanced Visualizations of Combined Data')
    additional_visualizations(combined_data)
    
    # combined_data = analyze_overlaps(setlist_data, spotify_data, tracks, 'Artist')
    # st.header('Combined Artist Table with Albums')
    # st.write(combined_data)

     # Display trends
    if not combined_data.empty:
        st.header('Trends Analysis')
        display_trends(combined_data)

    
    # overlaps = analyze_overlaps(setlist_data, spotify_data, 'Artist')
    # st.header('Overlaps in Artists')
    # st.write(overlaps)
    # st.header('Combined Artist Table with Albums')
    # st.write(combined_data)
    
    # st.header('Song Popularity Analysis')
    # plot_data(tracks)

if __name__ == "__main__":
    main()
