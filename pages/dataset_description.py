import streamlit as st

def app():
    st.title('Dataset Description')

    # Using markdown for better text formatting and readability
    st.markdown("""
## DATA SOURCE 1: Spotify API
- **API Docs:** [Spotify Web API Documentation](https://developer.spotify.com/documentation/web-api)
- **Description:** 
    Spotify's Web API provides detailed account data on tracks, artists, albums, and playlists. This includes audio features like valence, energy, danceability, and popularity scores for tracks. The API allows for exploration of how these features correlate with a song's success and public reception.
    - **Rate Limiting:** Spotify notes that rate limits may vary depending on the endpoint, the user's subscription type, or other factors. They implement rate limiting to ensure fair usage of the API among all users. Standard HTTP status codes are used to indicate rate limiting. If the rate limit is hit, Spotify's API will return a `429 Too Many Requests` status code, including a `Retry-After` header in the response, indicating how many seconds to wait before making a new request.
    - **Authentication:** Requires OAuth 2.0 authentication.

## DATA SOURCE 2: Setlist.fm Scrape-able Data
- **URL:** [Setlist.fm](https://www.setlist.fm)
- **Description:** 
    Setlist.fm is a user-maintained database of concert setlists and artist touring schedules worldwide. By scraping this site, data can be collected on live performance frequency, methods of song selection for concerts, and artists' touring patterns. This requires automation to obtain and structure, including artist names, songs played, concert dates, and locations. To scrape this data, it was necessary to look into html tags and text formatting to obtain scrape-able data that could be replicated with different artists.

## DATA SOURCE 3: Kaggle Spotify Dataset
- **URL:** [Kaggle Spotify Dataset](https://www.kaggle.com/datasets/fcpercival/160k-spotify-songs-sorted/data)
- **Description:** 
    This comprehensive dataset from Kaggle includes over 160,000 tracks with attributes such as acousticness, danceability, energy, and valence. It offers a historical perspective on music trends and characteristics, providing a foundation for analyzing the evolution of popular music features.
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    app()
