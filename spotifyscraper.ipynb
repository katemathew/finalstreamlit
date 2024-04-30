from sqlalchemy import create_engine, Column, String, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import os

# Ensure all your other imports and your robust_fetch, Artist, Album, Track classes remain unchanged.

def main():
    client_id = '5b2023b50cd44ccca291f436252f1381'
    client_secret = 'b87bc93755134e1e97bf139ca8855ca7'
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
    database_url = os.environ.get("postgres://u4ja2bod19v7gd:p9e70065bd97ea89a78fd91429d857f1c6dcb32c248a847c624d3a359bdeba876@ce1r1ldap2qd4b.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/db3gjtci88doqv")  # Assuming you've set this environment variable in Heroku
    engine = create_engine(database_url)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    # Remaining part of your code where you fetch data and populate the database
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
