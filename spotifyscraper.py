import os
import logging
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
load_dotenv()

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

def main():
    client_id = ''
    client_secret = ''
    artist_uris = {
        'Taylor Swift': 'spotify:artist:06HL4z0CvFAxyc27GXpf02',
        'Bad Bunny': 'spotify:artist:4q3ewBCX7sLwd24euuV69X',
        'The Weeknd': 'spotify:artist:1Xyo4u8uXC1ZmMpatF05PJ',
        'Drake': 'spotify:artist:3TVXtAsR1Inumwj472S9r4',
        'Peso Pluma': 'spotify:artist:12GqGscKJx3aE4t07u7eVZ'
    }

    credentials = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(client_credentials_manager=credentials)

    # Connect to Heroku PostgreSQL database
    database_url = os.getenv("DATABASE_URL").replace("postgres://", "postgresql://")
    engine = create_engine(database_url)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

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

if __name__ == "__main__":
    main()
