import streamlit as st

def app():
    st.title('Webapp Reflection Page')

    st.header("Project Overview")
    st.write("""
    What did you set out to study? (i.e., what was the point of your project? This should be close to your Milestone 1 assignment, but if you switched gears or changed things, note it here.)
    """)

    st.header("Discoveries and Conclusions")
    st.write("""
    What did you discover/what were your conclusions (i.e., what were your findings? Were your original assumptions confirmed, etc.?)
    """)

    st.header("Challenges")
    st.write("""
    What difficulties did you have in completing the project?
    """)

    st.header("Skills Wishlist")
    st.write("""
    What skills did you wish you had while you were doing the project?
    """)

    st.header("Future Directions")
    st.write("""
    What would you do “next” to expand or augment the project?
    """)

    st.header("Dataset Description")
    st.write("""
    Finally, you should have a tab that’s basically a description of your datasets. This should be similar to what you submitted for Milestone 1.
    """)

if __name__ == "__main__":
    app()
