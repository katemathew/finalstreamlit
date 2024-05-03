import os
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from sqlalchemy import create_engine, Column, String, Integer, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
#from dotenv import load_dotenv
import logging
import spotipy
import seaborn as sns
import altair as alt
from spotipy.oauth2 import SpotifyClientCredentials

# Load environment variables from .env file
#load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)

def create_database_tables(engine):
    Base.metadata.create_all(engine)
# Database schema setup
Base = declarative_base()

#Trouble Setting Up Environment, Keep Code For Further Security/Optimization

class Artist(Base):
    __tablename__ = 'artists'
    id = Column(String, primary_key=True)
    name = Column(String)
    albums = relationship("Album", back_populates="artist")

class Album(Base):
    __tablename__ = 'albums'
    id = Column(String, primary_key=True)
    name = Column(String)
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



def clean_artist_name(name):
    """Clean artist names by removing unwanted characters and making them lowercase."""
    return name.replace('[', '').replace(']', '').replace("'", "").strip().lower()

def display_trends(df):
    if df.empty:
        st.write("No data available for analysis.")
        return
    
    # Initialize dictionary to store names and average values
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

    # Loop through dictionary, calculate mean, display results
    for metric, display_name in metrics.items():
        if metric in df.columns:
            average_value = df[metric].mean()
            st.write(f"**Average {display_name}:** {average_value:.2f}")
        else:
            st.write(f"{display_name} data not available.")


def fetch_artist_albums(artist_id):
    # Fetch all albums by the artist
    #results = sp.artist_albums(artist_id, album_type='album,single', limit=20)
    results = sp.artist_albums(artist_id, album_type=None, country=None, limit=20, offset=0)
    albums = results['items']
    while results['next']:  # Continue fetching next page if available
        results = sp.next(results)
        albums.extend(results['items'])
    return albums

def fetch_album_tracks(album_id):
    # Fetch all tracks from an album
    results = sp.album_tracks(album_id)
    tracks = results['items']
    while results['next']:  # Continue fetching next page if available
        results = sp.next(results)
        tracks.extend(results['items'])
    return tracks

def fetch_and_save_spotify_data():
    artist_uris = {
        
        'Taylor Swift': '06HL4z0CvFAxyc27GXpf02',
        'Bad Bunny': 'spotify:artist:4q3ewBCX7sLwd24euuV69X',
        'The Weeknd': 'spotify:artist:1Xyo4u8uXC1ZmMpatF05PJ',
        'Drake': 'spotify:artist:3TVXtAsR1Inumwj472S9r4'
    }
    # 'Morgan Wallen': 'spotify:artist:4oUHIQIBe0LHzYfvXNW4QM',
    # 'Peso Pluma': 'spotify:artist:12GqGscKJx3aE4t07u7eVZ',
    #     'Metro Boomin': 'spotify:artist:0iEtIxbK0KxaSlF7G42ZOp',
    #     'Karol G': 'spotify:artist:790FomKkXshlbRYZFtlgla',
    #     'Future': 'spotify:artist:1RyvyyTE3xzB2ZywiAwp0i',
    #     'Tame Impala': 'spotify:artist:5INjqkS1o8h1imAzPqGZBb'
    database_url = "postgresql://u4ja2bod19v7gd:p9e70065bd97ea89a78fd91429d857f1c6dcb32c248a847c624d3a359bdeba876@ce1r1ldap2qd4b.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/db3gjtci88doqv"
    sp = spotipy.Spotify(client_credentials_manager=credentials)
    # Database connection setup
    engine = create_engine(database_url)
    connection = engine.connect()
    create_database_tables(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    # all_tracks = []  # List to store track dictionaries for CSV output
    for artist_name, artist_uri in artist_uris.items():
        print(artist_name + artist_uri)
        try:
            albums = fetch_artist_albums(artist_uri)
            for album in albums:
                print(album['id'])
                tracks = fetch_album_tracks(album['id'])
                for track in tracks:
                    try:
                        print(track[id])
                        # Ensuring each artist and album is only added once
                        artist = session.query(Artist).filter_by(id=track['artists'][0]['id']).first()
                        if not artist:
                            artist = Artist(id=track['artists'][0]['id'], name=track['artists'][0]['name'])
                            session.add(artist)
                        album_record = session.query(Album).filter_by(id=album['id']).first()
                        if not album_record:
                            album_record = Album(id=album['id'], name=album['name'], artist_id=artist.id)
                            session.add(album_record)
                        # Checking for the existence of the track
                        track_record = session.query(Track).filter_by(id=track['id']).first()
                        if not track_record:
                            track_record = Track(id=track['id'], name=track['name'], popularity=track.get('popularity', 0), duration_ms=track['duration_ms'], album_id=album_record.id)
                            session.add(track_record)
                            # Append track info to list for CSV
                            all_tracks.append({
                                'Track ID': track['id'],
                                'Track Name': track['name'],
                                'Popularity': track.get('popularity', 0),
                                'Duration (ms)': track['duration_ms'],
                                'Album ID': album_record.id
                            })
                    except Exception as e:
                        logging.error(f"Error processing track data for {artist_name}: {e}")
            session.commit()  # Committing after processing each artist to manage transaction sizes
        except Exception as e:
            logging.error(f"Error fetching data for {artist_name}: {e}")
            session.rollback()  # Rolling back in case of failure
    session.close()  # Closing the session after all processing is done
    if all_tracks:
        df_tracks = pd.DataFrame(all_tracks)
        df_tracks.to_csv('tracks_data.csv', index=False)
        logging.info("Tracks data has been saved to CSV.")


def load_setlist_data():
    df = pd.read_csv('setlist_data.csv')
    # Ensure the column 'Artist' exists and apply name cleaning
    df['Artist'] = df['Artist'].apply(clean_artist_name)
    # Rename 'Songs' column to 'name'
    df.rename(columns={'Songs': 'name'}, inplace=True)
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

def analyze_overlaps(df1, df2, df3, key):
    combined_kaggle_spotify = pd.merge(df2, df3, on=key, how='inner')
    st.header('kaggle and spotify')
    st.write(combined_kaggle_spotify.head(15))
    combined_data = pd.merge(df1, combined_kaggle_spotify, on=key, how='outer')
    #final_combined_data = pd.merge(combined_data, df3, on=key, how='inner')
    return combined_data


def plot_data(df):
    if df.empty:
        st.write("No data available to plot.")
        return

    if 'popularity' in df.columns:
        bins = st.slider("Select number of bins for histogram:", min_value=10, max_value=100, value=20, step=5)
        
        # Create a new figure and axes
        fig, ax = plt.subplots()
        
        # Plotting the histogram
        df['popularity'].hist(ax=ax, bins=bins)
        ax.set_xlabel('Popularity')
        ax.set_ylabel('Frequency')
        
        # Display the plot in Streamlit
        st.pyplot(fig)
    else:
        st.error('The "popularity" column is not present in the dataset.')
def popularity_distribution_box_plot(df):
    if df.empty:
        st.write("No data available to plot.")
        return

    # Box Plot for Track Popularity
    if 'popularity' in df.columns:
        fig, ax = plt.subplots()
        df['popularity'].plot(kind='box', ax=ax)
        ax.set_title('Popularity Distribution')
        ax.set_ylabel('Popularity Score')
        st.pyplot(fig)

def popularity_versus_track_duration_scatter_plot(df):
    if df.empty:
        st.write("No data available to plot.")
        return

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

def time_series_plot_pop_over_time(df):
    if df.empty:
        st.write("No data available for plot.")
        return

    # Time Series Plot for Popularity Over Time
    if 'release_date' in df.columns and 'popularity' in df.columns:
        # Date
        df['release_date'] = pd.to_datetime(df['release_date'], format='%m/%d/%y', errors='coerce')
        time_data = df.dropna(subset=['release_date', 'popularity'])
        time_data = time_data.sort_values('release_date')

        # Plot
        fig, ax = plt.subplots()
        sns.lineplot(x='release_date', y='popularity', data=time_data, ax=ax)
        ax.set_title('Popularity Over Time')
        ax.set_xlabel('Release Date')
        ax.set_ylabel('Popularity')
        st.pyplot(fig)

def pie_chart_album_contribution(df):
    if df.empty:
        st.write("No data available for plot.")
        return
    
    # Pie Chart for Album Contribution
    if 'Album' in df.columns and 'popularity' in df.columns:
        album_contribution = df.groupby('Album')['popularity'].sum()
        fig, ax = plt.subplots()
        album_contribution.plot(kind='pie', ax=ax, autopct='%1.1f%%')
        ax.set_title('Recent Album Contribution to Overall Popularity')
        ax.set_ylabel('')
        st.pyplot(fig)


def correlation_heatmap(df):
    if df.empty:
        st.error("DataFrame is empty. No data to display.")
        return
    
    cols_to_check = ['popularity', 'duration_ms', 'energy', 'danceability', 'acousticness', 'valence']
    cols_available = [col for col in cols_to_check if col in df.columns]
    
    if not cols_available:
        st.error("None of the specified columns are available in the DataFrame.")
        return

    correlation_data = df[cols_available]
    correlation = correlation_data.corr()

    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(correlation, annot=True, cmap='coolwarm', ax=ax, fmt=".2f")
    ax.set_title('Correlation Heatmap')
    st.pyplot(fig) 


def interactive_scatter_plot(df):
    if df.empty:
        st.write("No data available for plot.")
        return

    # User Selection
    x_options = df.select_dtypes(include=['float64', 'int']).columns.tolist()
    y_options = x_options
    x_axis = st.selectbox("Choose X-axis", options=x_options, index=x_options.index('duration_ms'))
    y_axis = st.selectbox("Choose Y-axis", options=y_options, index=y_options.index('popularity'))

    # Plot
    chart = alt.Chart(df).mark_circle(size=60).encode(
        x=x_axis,
        y=y_axis,
        tooltip=[x_axis, y_axis]
    ).interactive()

    st.altair_chart(chart, use_container_width=True)

def interactive_time_series(df):
    if df.empty or 'release_date' not in df.columns:
        st.write("No data available for plot.")
        return

    # Format
    df['release_date'] = pd.to_datetime(df['release_date'], format='%m/%d/%y', errors='coerce')
    df = df.sort_values('release_date')

    # NaT (not a time) 
    if df['release_date'].isnull().any():
        st.write("Some dates could not be parsed.")
        df = df.dropna(subset=['release_date'])

    # Slider for selecting years
    min_year = int(df['release_date'].dt.year.min())
    max_year = int(df['release_date'].dt.year.max())
    year_to_view = st.slider("Select Year", min_value=min_year, max_value=max_year, value=min_year)

    # Filter data based on year
    filtered_data = df[df['release_date'].dt.year == year_to_view]
    
    # Check if filtered data is empty
    if filtered_data.empty:
        st.write("No data available for the selected year.")
        return

    fig, ax = plt.subplots()
    sns.lineplot(x='release_date', y='popularity', data=filtered_data, ax=ax)
    ax.set_title(f'Popularity Over Time in {year_to_view}')
    ax.set_xlabel('Release Date')
    ax.set_ylabel('Popularity')
    st.pyplot(fig)

        
def main():
    st.title('Music Data Analysis App')
    st.subheader('Kate Mathew')

    # Instructions
    with st.expander("**Welcome to my Music Data Analysis App, Start Here!**"):
        st.write("""
        There is a lot you can do here to explore trends with artists and songs. First, if you want to explore what each data table/data collection source looks like individually, there are dropdowns for each individual scraper to see how they collect information. Now on to the fun stuff! 
        
        To get started, select an artist from the dropdown. These artists were chosen as a combination from recently scraped setlist data and the most popular artists on Spotify currently. Once you have your artist selected, there are many things you can explore:
        
        1. **Combined Dataset for The Artist** - This shows how the three datasets merge together, which will be used for further analysis and visualization.
        2. **Frequency of Song Popularity** - Shows frequency of track's popularity for an Artist using their Spotify Popularity Score. Feel free to use the slider to change the bin size and explore the data more broadly!
        3. **Popularity Distribution Box Plot** - Shows The Average Range For Popularity Scores For An Artist, As Well As Outliers.
        4. **Popularity vs Track Duration Scatter Plot** - Looks At Artist Data and Shows If There Are Any Trends Within Track Duration and Popularity.
        5. **Correlation Heat Map** - Shows how strong relationships are between track characteristics.
        6. **Popularity over Time Time Series Plot** - Looks At Trends Between Popularity and Release Date
        7. **Album Popularity Contribution Pie Chart** - Pie Chart Showing Recent Album Contribution and Popularity.
        8. **Interactive Scatter Plot** - Explore on your own! Choose two variables and see how they correlate.
        9. **Interactive Time Series Analysis** - Feel free to explore time with the slider and see how popularity and release date correlate!
        10. **Trend Analysis** - Finally, There is an average trend analysis for the curious folks! 
        
        Thanks for exploring!
        """)

     # Findings 
    with st.expander("**Findings**"):
        st.write("""
        My analysis reveals certain trends and artist-specific tendencies that highlight the intersection between various musical attributes and song popularity. It is important to note the subjectivity of music, and while there were general and artist based trends, many aspects of songs and popularity cannot be measured easily, as there are outside factors that can influence these decisions. Here are some key insights:

        **General Trends:**
        - **Duration vs. Popularity:** Observed a general trend where shorter song durations correlate with higher popularity, as indicated by a negative correlation of -0.61. This trend aligns with current listener preferences for shorter tracks, likely influenced by shorter attention spans. However, notable exceptions such as Taylor Swift’s "All Too Well (10 Minute Version)" demonstrate that long tracks can also achieve significant popularity.

        **Energy and Acoustics:**
        - Tracks with lower acoustic features typically exhibit higher energy levels. This suggests a preference for more electronically produced or upbeat music, which can vary significantly across different musical genres.

        **Artist-Specific Observations:**
        - **Taylor Swift:** For Taylor Swift, the link between track duration and popularity is particularly pronounced, providing insights into her song production strategy and its impact on commercial success.
        - **Drake:** Drake's tracks show weaker overall correlations, highlighting the diversity in his musical style. Notably, a negative correlation between energy and danceability in his music suggests that higher energy does not always enhance danceability, possibly due to the genre of rap, lyrical focus, or complex rhythms that characterize his songs.

        These insights can be instrumental for artists, producers, and music platforms in making informed decisions about song production and curation. I encourage you to explore the correlation heatmap to uncover additional insights and understand how various musical elements interact across different artists and genres. Dive into the analysis and see what unique correlations resonate with or challenge your understanding of music!
    """) 
    # Gotchas
    with st.expander("**Awh Darns! Gotcha**"):
        st.write("""
        - **Environmental Variables & Security**: Even after establishing environmental variables to protect sensitive information and testing locally, when brought to Github and Streamlit Share, the variables were not found in the app.
        - **Multipage Scraper**: There was trouble scraping data that had pagination incorporated as well as undefined html variables, especially when it was not consistent throughout the website.
        - **Heroku Database & CSV’s**: Limited capacity.
        - **Variable Consistency in Combined Dataset**: As this data is compiled by multiple sources, there are parts of the combined dataset that will duplicate or not match up, as they refer to different variables and correlations depending on where they are scraped from.
        """)

    
    setlist_data = load_setlist_data()
    spotify_data = load_filtered_spotify_data()
    tracks = load_spotify_tracks_db()

    # Setlist Data Expander
    with st.expander("**Setlist Data** - This data was retrieved from setlist.fm, a top site for discovering features for live events. Click To Explore A Few Lines."):
        st.write(setlist_data.head())

    # Spotify Filtered Data Expander
    with st.expander("**Kaggle: Spotify Filtered Data** - This data was retrieved from a Kaggle dataset, compiling Spotify data from the 2000's to 2020. Click To Explore A Few Lines."):
        st.write(spotify_data.head())

    # Spotify Tracks Data Expander
    with st.expander("**Spotify Tracks Data** - This data was retrieved from the Spotify API, providing current metrics for songs and artists. Click To Explore A Few Lines."):
        st.write(tracks.head(50))


    # Define a list of allowed artists
    allowed_artists = ["taylor swift", "drake", "the weeknd", "bad bunny"]

    # Filter the artist list to include only the allowed artists
    artist_list = [artist for artist in tracks['Artist'].unique() if artist.lower() in allowed_artists]

    # Artist selection dropdown
    selected_artist = st.selectbox('**Select an Artist**', artist_list)

    # Filter data by selected artist
    filtered_setlist_data = setlist_data[setlist_data['Artist'] == selected_artist]
    filtered_setlist_data = filtered_setlist_data.drop(columns='Artist')

    filtered_spotify_data = spotify_data[spotify_data['Artist'] == selected_artist]
    filtered_spotify_data = filtered_spotify_data.drop_duplicates(subset='name', keep='first').drop(columns=['duration_ms', 'popularity', 'id', 'artists', 'Artist'])

    filtered_tracks = tracks[tracks['Artist'] == selected_artist]
    filtered_tracks = filtered_tracks.drop(columns='track_id').sort_values('name')

    st.header('setlist')
    st.write(filtered_setlist_data)
    st.header('kaggle')
    st.write(filtered_spotify_data)
    st.header('spotify')
    st.write(filtered_tracks)

    # Display Combined Data for selected artist
    st.header(f'Combined Data for {selected_artist}')
    combined_data = analyze_overlaps(filtered_setlist_data, filtered_spotify_data, filtered_tracks, 'name')
    st.write(combined_data)

    # Explanation about Spotify Popularity Index
    st.header(f'Visualizations for {selected_artist}')
    st.markdown("""
    **The Spotify Popularity Index** is a 0-to-100 score that ranks how popular an artist is relative to other artists on Spotify. As your numbers grow, you'll get placed in more editorial playlists and increase your reach on algorithmic playlists and recommendations.
    """)

    st.header('Frequency of Song Popularity')
    plot_data(filtered_tracks)

    
    st.header('Popularity Distribution Box Plot')
    popularity_distribution_box_plot(filtered_tracks)
    st.header('Popularity vs Track Duration Scatter Plot')
    popularity_versus_track_duration_scatter_plot(filtered_tracks)
    # plot_alternative_visualizations(filtered_tracks)

    if not combined_data.empty and {'popularity', 'duration_ms'}.issubset(combined_data.columns):
        st.header('Correlation Heatmap of Combined Data')
        correlation_heatmap(combined_data)
    else:
        st.error('Data not suitable for correlation heatmap.')
    
    st.header('Album Popularity Contribution Pie Chart')
    pie_chart_album_contribution(combined_data)

    st.header('Popularity over Time Time Series Plot')
    time_series_plot_pop_over_time(combined_data)

    # # Advanced Visualizations
    # st.header('Advanced Visualizations of Combined Data')
    # additional_visualizations(combined_data)

    st.header('Interactive Scatter Plot')
    interactive_scatter_plot(combined_data)

    st.header('Interactive Time Series Analysis')
    interactive_time_series(combined_data)

     # Trends
    if not combined_data.empty:
        st.header('Trends Analysis')
        display_trends(combined_data)


if __name__ == "__main__":
    main()
