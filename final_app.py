import os
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from sqlalchemy import create_engine, Column, String, Integer, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from dotenv import load_dotenv
import logging
import spotipy
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

def fetch_and_save_spotify_data():
    artist_uris = {
        'Taylor Swift': 'spotify:artist:06HL4z0CvFAxyc27GXpf02',
        'Bad Bunny': 'spotify:artist:4q3ewBCX7sLwd24euuV69X',
        'The Weeknd': 'spotify:artist:1Xyo4u8uXC1ZmMpatF05PJ',
        'Drake': 'spotify:artist:3TVXtAsR1Inumwj472S9r4',
        'Peso Pluma': 'spotify:artist:12GqGscKJx3aE4t07u7eVZ'
    }

    database_url = "postgresql://u4ja2bod19v7gd:p9e70065bd97ea89a78fd91429d857f1c6dcb32c248a847c624d3a359bdeba876@ce1r1ldap2qd4b.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/db3gjtci88doqv"

    # Database connection setup
    engine = create_engine(database_url)
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        for artist_name, artist_uri in artist_uris.items():
            tracks_data = fetch_artist_top_tracks(artist_uri)
            for data in tracks_data:
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
            session.commit()
            logging.info(f"Data for {artist_name} successfully saved to the database")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        session.rollback()
    finally:
        session.close()

# Remaining functions remain unchanged


def load_setlist_data():
    df = pd.read_csv('setlist_data.csv')
    df.rename(columns={'Artist Name': 'Artist'}, inplace=True)
    return df

def load_filtered_spotify_data():
    df = pd.read_csv('filtered_spotify_data.csv')
    df['Artist'] = df['artists'].str.replace(r"\[|\]|'", "")
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
                Track.name.label('track_name'),
                Track.popularity,
                Track.duration_ms,
                Album.name.label('album_name'),
                Artist.name.label('artist_name')
            )
            .select_from(Track)
            .join(Album, Track.album_id == Album.id)
            .join(Artist, Album.artist_id == Artist.id)
            .statement, 
            engine
        )
    finally:
        session.close()

    return tracks

def analyze_overlaps(df1, df2, key='Artist'):
    return pd.merge(df1, df2, on=key, how='inner')

def plot_data(df):
    if df.empty:
        st.write("No data available to plot.")
        return
    fig, ax = plt.subplots()
    df['popularity'].hist(ax=ax)
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
    overlaps = analyze_overlaps(setlist_data, spotify_data, 'Artist')
    st.header('Overlaps in Artists')
    st.write(overlaps)
    st.header('Song Popularity Analysis')
    plot_data(tracks)

if __name__ == "__main__":
    main()
