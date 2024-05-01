pages/webappquestions.py

import streamlit as st

def app():
    st.title('Webapp Reflection Page')
    st.write("""
    What did you set out to study?  (i.e., what was the point of your project? This should be close to your Milestone 1 assignment, but if you switched gears or changed things, note it here.)
    What did you Discover/what were your conclusions (i.e., what were your findings? Were your original assumptions confirmed, etc.?)
    What difficulties did you have in completing the project?
    What skills did you wish you had while you were doing the project?
    What would you do “next” to expand or augment the project?
    
    Finally, you should have a tab that’s basically a description of your datasets. This should be similar to what you submitted for Milestone 1.
    """)

if __name__ == "__main__":
    app()
