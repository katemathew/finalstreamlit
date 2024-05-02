import streamlit as st

def app():
    st.title('Webapp Reflection Page')

    st.header("Project Overview")
    st.write("""
    **What did you set out to study?** (i.e., what was the point of your project? This should be close to your Milestone 1 assignment, but if you switched gears or changed things, note it here.)
    
    The goal of this project was to uncover trends in songs that achieve high popularity scores on Spotify as well as are performed frequently live. By correlating live performance data from Setlist.FM with Spotify's popularity index and audio features, I wanted to discover if there were certain characteristics that might influence a song’s success, potential future success, and how that correlates in the live event space. This analysis had the goal to reveal trends in music preferences, offering insights into the evolving landscape of popular music and live concerts. Ultimately, I wanted to identify the key features that contribute to a song's success, both in the digital realm and in live settings, providing a deeper understanding of current music trends and audience preferences.

    These three datasets (Setlist.FM, Kaggle, and Spotify API) were integrated to examine the relationship between live performance, popularity, and audio features of songs. By matching songs and artists from Setlist.fm with corresponding Spotify API data, I wanted to analyze which audio features are most prevalent in live performances. Furthermore, the Kaggle Spotify dataset allowed for a historical comparison, identifying trending characteristics of popular live music, and if they have evolved over the years. This combination offers a unique lens to study the dynamics of music popularity, both in recorded and live formats, and how certain music features can influence a song. The Kaggle dataset provided a broad historical dataset of songs, which can be invaluable for longitudinal studies, trend analysis over decades, genre evolution, and more. The Spotify API allowed access to current data, including the latest songs, albums, and artist information. The Spotify API worked well in tandem with the Kaggle dataset for the most recent data and real-time analysis. These both were useful when comparing to Setlist.fm, especially when looking into song selection for their sets. 
    This field is particularly important to me, as I am currently developing a music software based platform, and the findings from this project will have great insights on what direction I should move forward with in the music space. Additionally, I really enjoyed working on this project with my personal curiosity and investment in the music industry. Fun fact, I play 7 instruments and used to work at Universal Music Group!
    """)

    st.header("Discoveries and Conclusions")
    st.write("""
    **What did you discover/what were your conclusions?** (i.e., what were your findings? Were your original assumptions confirmed, etc.?)
    
    My analysis revealed certain trends and artist-specific tendencies that highlight the intersection between various musical attributes and song popularity. It is important to note the subjectivity of music, and while there were general and artist based trends, many aspects of songs and popularity cannot be measured easily, as there are outside factors that can influence these decisions. Additionally, in the live entertainment space, many songs are chosen for their high danceability, energy, popularity from the artist, or from a new release, which was portrayed in the data, however, this is very subjective as well.
    Here are some key insights:
    - **General Trends:**
      - **Duration vs. Popularity:** Observed a general trend where shorter song durations correlate with higher popularity, as indicated by a negative correlation of -0.61. This trend aligns with current listener preferences for shorter tracks, likely influenced by shorter attention spans. However, notable exceptions such as Taylor Swift’s "All Too Well (10 Minute Version)" demonstrate that long tracks can also achieve significant popularity.
    - **Energy and Acoustics:**
      - Tracks with lower acoustic features typically exhibit higher energy levels. This suggests a preference for more electronically produced or upbeat music, which can vary significantly across different musical genres.
    - **Artist-Specific Observations:**
      - **Taylor Swift:** For Taylor Swift, the link between track duration and popularity is particularly pronounced, providing insights into her song production strategy and its impact on commercial success.
      - **Drake:** Drake's tracks show weaker overall correlations, highlighting the diversity in his musical style. Notably, a negative correlation between energy and danceability in his music suggests that higher energy does not always enhance danceability, possibly due to the genre of rap, lyrical focus, or complex rhythms that characterize his songs.
    - It was extremely interesting to look at patterns for a specific artist, however, general trends were harder to identify. This does bring it back to the fundamentals, that music is an art, and while there are certain attributes that correlate, there is an extremely subjective part of this process. Additionally, it is necessary to factor in outside popularity from marketing, social platforms, existing fan bases, etc. I do believe that my findings were useful and answered the questions I sought out to find in my initial goal. There are trends in song popularity, on an artist level and generally, and these characteristics could be mirrored in the future, allowing an artist to make a new hit with information on what made them successful in the past. Additionally, this data would be good to consider in terms of selecting singles for artists, marketing, finding artists with similar patterns, and for song production, utilizing average values of an artist’s previously popular songs. Live performance appeal, as I mentioned above, is a bit harder to calculate, however, trends in danceability, popularity, energy, acoustics, and valence do help us see how wide the selection of songs can be.
    """)

    st.header("Challenges")
    st.write("""
    **What difficulties did you have in completing the project?**
    
    I was able to learn a lot while completing this project. First, I was not familiar with OAuth Authorization and Database Storage Systems, specifically Heroku. Setting these systems up and implementing them into my code took a long time, as I did not understand the fundamentals of this kind of system too well. Similarly, I decided to use chromedriver to assist with my web scraping, and learning how to utilize this with the data I wanted to collect was challenging. I mentioned this on the main page as well, but scraping from the web turned out to be pretty difficult, as there were some aspects of the page that were not well defined with html tags, or were in a more general tag (ex: artist + location + date in one), where I would have to code the scraper to break up these sections. Additionally, if there were multiple pages of results or if I was trying to use the scraper to search for multiple artists, it was difficult to determine a link that was uniform or that I could plug a name into, as many of them had unique tags at the end. After the data collection, combining the data proved to be a difficult task, as the three datasets had different labels for categories (ex. Artist or artist_name, song or track). I did have SQL knowledge from a prior class, so this proved useful, where I could make all of the categories in this section ‘Artist’ and have that be the commonality to combine the datasets. This still required a lot of trial and error to find what worked best, for example, the artist names were presented differently in each dataset, so I had to clean the data as well. The easiest way to do this was through a clean function, making all of the text in the Artist section of the data tables standardized. Once I was able to combine the three datasets, I moved on to analyzing the data. Visualizing the data was vital in the trend identification process, especially with the amount of data that was collected. Once I understood how streamlit visualizations worked (which took a fair bit of time), I was able to test out different formats to see what worked best to present my data.
    """)

    st.header("Skills Wishlist")
    st.write("""
    **What skills did you wish you had while you were doing the project?**
   
    **Debugging and Familiarity With Github and Streamlit**: This was the most time-consuming aspect of the project, especially when trying to combine datasets with different names, upload them to Github, and then create the streamlit app, which caused many disconnects. 
    
    **Advanced Math**: In the future, I would like to employ more math-based insights into my data analysis and visualizations. I was able to use my knowledge from statistics, but a deeper foundation in math would be useful.
    """)

    st.header("Future Directions")
    st.write("""
    **What would you do “next” to expand or augment the project?**
    
    In the future, I would love to expand this project by having a search button on the app, allowing a user to search up any artist of their choosing, have the scrapers live scrape data from the three established datasets as well as others, and return the data to the user. Additionally, I would like to compare artists that have the same patterns with their data, as well as have forecasting data for how they could increase popularity in the future. It would also be interesting to find and apply a quantitative factor to a qualitative measurement to incorporate those into artist trends and popularity as well.
    """)

if __name__ == "__main__":
    app()
