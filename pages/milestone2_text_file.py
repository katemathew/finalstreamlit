import streamlit as st

def app():
    st.title('Navigating Zip File & Data Modeling Insights')

    st.write("""Milestone 2 Text File (milestone2_text_file.py): I wanted to include the Milestone 2 text file as well that was missing from the original zip submission, not sure what happened!""")

    # Navigating Zip File Section
    st.header("Navigating Zip File")
    st.write("""
    - **Kaggle:** Filters and sorts through downloadable Spotify Kaggle dataset.
    - **Kaggle Combined:** Correlates Kaggle dataset with Setlist FM scraper data to find correlations.
    - **Spotify API:** Looks for specified artists, songs, and associated features through Spotify API.
    - **Setlist FM Setlist Scraper [Original]:** Goes through an artist’s specific setlist to scrape data.
    - **Setlist FM Artist Page Scraper:** Goes to Setlist FM Artist page and scrapes data from the most recent setlists/performances.
    """)

    # Strengths of Data Modeling Formats Section
    st.header("Strengths of Data Modeling Formats")
    st.write("""
    - **Flexibility and Scalability:** The use of Python libraries like pandas for data manipulation and SQLAlchemy for database management allows scalable and flexible data processing. These tools are well-suited for handling both small and large datasets.
    - **Structured Data Storage:** Using structured data formats (CSVs for simple datasets and relational databases for more complex relationships) facilitates systematic storage and retrieval of data.
    - **Automated Data Collection:** Scripts employing web scraping (Selenium and BeautifulSoup) and API calls (Spotify API) enable automated and efficient data collection, reducing manual effort and improving data accuracy and freshness.
    - **Error Handling and Robustness:** Implementations such as retry logic in API interactions and basic error handling in web scraping scripts help improve the robustness of data collection processes.
    """)

    # Weaknesses of Data Modeling Formats Section
    st.header("Weaknesses of Data Modeling Formats")
    st.write("""
    - **Dependency on External Structures:** The data models heavily rely on the structure of external data sources (web pages, APIs). Changes in these sources can break the data collection scripts.
    - **Efficiency Concerns:** Using Selenium for web scraping is resource-intensive compared to direct HTTP requests. It's slower and more prone to errors caused by web page dynamics.
    - **Limited Complex Query Support:** While CSV files are easy to use and understand, they lack support for complex querying and data relationships, which are better handled by relational databases.
    - **Data Integrity and Maintenance:** Ensuring data integrity and maintaining updates across different sources can be challenging, especially when data schemas are altered or expanded.
    """)

    # Data Storage on Disk Section
    st.header("Data Storage on Disk")
    st.write("""
    - **CSV Files:** Simple, flat-file storage that is easy to read and write. Ideal for small datasets or situations where complex relationships between data are not a concern.
    - **SQLite Database:** Offers more sophisticated data management capabilities, such as enforcing data types, relationships, and integrity constraints. Better suited for complex and relational data handling.
    """)

    # Extending the Model with a New Data Source Section
    st.header("Extending the Model with a New Data Source")
    st.write("""
    1. **Assess The New Data Source:** Understand the structure and relevance of the new data. Determine how it links to existing data elements.
    2. **Schema Integration:** Depending on the new data's nature, adjust the existing database schema or data handling scripts to incorporate new tables or fields. This might involve creating new relationships or modifying existing ones.
    3. **Update Data Collection Scripts:** Integrate new data fetching logic into existing scripts, ensuring seamless data collection and storage.
    4. **Interface Adjustments:** Update user interface/API to reflect new data types and relationships to ensure users can access and interact with the new data effectively.
    """)

    # Adding a New Attribute to Data Section
    st.header("Adding a New Attribute to Data")
    st.write("""
    **Adding Artist Hometowns**
    1. **Data Model Update:** Add a new column, `hometown`, to the relevant table in the database (`Artist` table in the SQL database). For CSVs, add a new column header in the relevant file.
    2. **Data Collection Update:** Modify data collection scripts to include hometown information. This could involve additional API calls or web scraping tasks.
    3. **Data Integration:** Ensure that when artist data is collected, the hometown information is also fetched and stored. This might require additional parsing and data transformation steps.
    4. **Database Modifications:** Execute a schema migration to add the new column.
    """)

if __name__ == "__main__":
    app()
