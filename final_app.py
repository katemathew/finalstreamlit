import os
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from sqlalchemy import create_engine, Column, String, Integer, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
import logging
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Environment setup
load_dotenv()  # Ensure your .env file is in the correct location relative to this script
logging.basicConfig(level=logging.INFO)

# Database and Spotify Model Definitions
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

# Fetching top tracks from Spotify
def fetch_artist_top_tracks(sp, artist_uri):
    results = sp.artist_top_tracks(artist_uri)
    return [{
        'track_id': track['id'],
        'name': track['name'],
        'popularity': track['popularity'],
        'duration_ms': track['duration_ms'],
        'album_id': track['album']['id'],
        'album_name': track['album']['name'],
        'release_date': track['album']['release_date'],
        'artist_id': track['artists'][0]['id'],
        'artist_name': track['artists'][0]['name']
    } for track in results['tracks']]

# Saving data to the database
def fetch_and_save_spotify_data():
    database_url = os.getenv("DATABASE_URL")
    engine = create_engine(database_url)
    Session = sessionmaker(bind=engine)
    session = Session()

    credentials = SpotifyClientCredentials(client_id=os.getenv('SPOTIFY_CLIENT_ID'), 
                                           client_secret=os.getenv('SPOTIFY_CLIENT_SECRET'))
    sp = spotipy.Spotify(client_credentials_manager=credentials)

    artist_uris = {
        'Taylor Swift': 'spotify:artist:06HL4z0CvFAxyc27GXpf02',
        # Other artists...
    }

    try:
        for artist_name, artist_uri in artist_uris.items():
            tracks_data = fetch_artist_top_tracks(sp, artist_uri)
            for data in tracks_data:
                artist = session.query(Artist).filter_by(id=data['artist_id']).first() or Artist(**data)
                session.add(artist)
                # Similar handling for albums and tracks
            session.commit()
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        session.rollback()
    finally:
        session.close()

# Main function setup for Streamlit
def main():
    # Data fetching and display
    fetch_and_save_spotify_data()
    setlist_data = pd.read_csv('setlist_data.csv')
    spotify_data = pd.read_csv('filtered_spotify_data.csv')

    st.title('Music Data Analysis App')
    st.write(setlist_data.head())
    st.write(spotify_data.head())

    # Overlaps and visualization...
    st.header('Song Popularity Analysis')
    plot_data(spotify_data['popularity'])

if __name__ == "__main__":
    main()
