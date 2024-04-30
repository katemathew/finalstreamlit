import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine, Column, String, Integer, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from dotenv import load_dotenv, dotenv_values
import logging
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


# Load environment variables from .env file
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)

# Ensure other necessary imports and your robust_fetch, Artist, Album, Track classes are declared
Base = declarative_base()

from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

class Artist(Base):
    __tablename__ = 'artists'

    id = Column(String, primary_key=True)
    name = Column(String)

    # This relationship will allow you to access an artist's albums directly
    albums = relationship("Album", back_populates="artist")

class Album(Base):
    __tablename__ = 'albums'

    id = Column(String, primary_key=True)
    name = Column(String)
    release_date = Column(String)
    artist_id = Column(String, ForeignKey('artists.id'))

    # This relationship links back to the artist and to the tracks
    artist = relationship("Artist", back_populates="albums")
    tracks = relationship("Track", back_populates="album")

class Track(Base):
    __tablename__ = 'tracks'

    id = Column(String, primary_key=True)
    name = Column(String)
    popularity = Column(Integer)
    duration_ms = Column(Integer)
    album_id = Column(String, ForeignKey('albums.id'))

    # This relationship links back to the album
    album = relationship("Album", back_populates="tracks")

def fetch_artist_top_tracks(sp, artist_uri):
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
    database_url = "postgresql://u4ja2bod19v7gd:p9e70065bd97ea89a78fd91429d857f1c6dcb32c248a847c624d3a359bdeba876@ce1r1ldap2qd4b.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/db3gjtci88doqv"

    # Database connection setup
    engine = create_engine(database_url)
    Session = sessionmaker(bind=engine)
    session = Session()

    # Spotify client setup
    client_id = '5b2023b50cd44ccca291f436252f1381'
    client_secret = 'b87bc93755134e1e97bf139ca8855ca7'
    credentials = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(client_credentials_manager=credentials)

    artist_uris = {
        'Taylor Swift': 'spotify:artist:06HL4z0CvFAxyc27GXpf02',
        'Bad Bunny': 'spotify:artist:4q3ewBCX7sLwd24euuV69X',
        'The Weeknd': 'spotify:artist:1Xyo4u8uXC1ZmMpatF05PJ',
        'Drake': 'spotify:artist:3TVXtAsR1Inumwj472S9r4',
        'Peso Pluma': 'spotify:artist:12GqGscKJx3aE4t07u7eVZ'
    }

    try:
        for artist_name, artist_uri in artist_uris.items():
            tracks_data = fetch_artist_top_tracks(sp, artist_uri)
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

def load_setlist_data():
    df = pd.read_csv('setlist_data.csv')
    df.rename(columns={'Artist Name': 'Artist'}, inplace=True)
    return df

def load_filtered_spotify_data():
    df = pd.read_csv('filtered_spotify_data.csv')
    df.rename(columns={'artists': 'Artist'}, inplace=True)
    return df

def load_spotify_tracks_db():
    # Hardcoded database URL
    database_url = "postgresql://u4ja2bod19v7gd:p9e70065bd97ea89a78fd91429d857f1c6dcb32c248a847c624d3a359bdeba876@ce1r1ldap2qd4b.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/db3gjtci88doqv"

    # Database connection setup
    engine = create_engine(database_url)
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        # Explicitly specify the starting point and path for the joins
        from sqlalchemy.orm import aliased
        
        # Aliasing the tables might help in complex queries where same table is joined multiple times
        artist_alias = aliased(Artist)
        album_alias = aliased(Album)
        track_alias = aliased(Track)
        
        # Constructing the query
        query = session.query(
            track_alias.id.label('track_id'),
            track_alias.name.label('track_name'),
            track_alias.popularity,
            track_alias.duration_ms,
            album_alias.name.label('album_name'),
            artist_alias.name.label('artist_name')
        ).select_from(track_alias) \
        .join(album_alias, track_alias.album_id == album_alias.id) \
        .join(artist_alias, album_alias.artist_id == artist_alias.id)

        # Executing the query and loading into DataFrame
        tracks = pd.read_sql(query.statement, engine)

    finally:
        session.close()

    return tracks
# Analyze overlaps
def analyze_overlaps(df1, df2, key='Artist'):
    if key not in df1 or key not in df2:
        st.error(f"Key '{key}' is missing from one of the dataframes.")
        return pd.DataFrame()
    common_artists = set(df1[key]).intersection(set(df2[key]))
    if not common_artists:
        st.write("No common artists found for merging.")
        return pd.DataFrame()
    return pd.merge(df1, df2, on=key, how='inner')


# Visualization
def plot_data(df):
    if df.empty:
        st.write("No data available to plot.")
        return

    # Create a new figure and axes
    fig, ax = plt.subplots()
    df['popularity'].hist(ax=ax)
    st.pyplot(fig)


# Main function for Streamlit
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

    st.write(setlist_data['Artist'].unique())
    st.write(spotify_data['Artist'].unique())

    setlist_data['Artist'] = setlist_data['Artist'].str.strip().str.title()
    spotify_data['Artist'] = spotify_data['Artist'].str.strip().str.title()

    overlaps = analyze_overlaps(setlist_data, spotify_data, 'Artist')
    st.header('Overlaps in Artists')
    st.write(overlaps)

    st.header('Song Popularity Analysis')
    plot_data(tracks)

if __name__ == "__main__":
    main()
