import streamlit as st


def about():
    st.markdown(
        """
        [**Marple**](https://www.marpledata.com/) is a software platform that specializes in the processing, visualization, and analysis of large time
        series data sets typically used in engineering and R&D. Think about visualizing & analyzing the data coming from your sensors,
        in a cloud platform!
        A public sharing link can be used to share your visualization view with people outside of your workspace, or even without a Marple account.

        They will get a limited view of your current data
        
        This Streamlit app uses Marple's SDK to demo the Public Share Links feature on running data from Garmin watches.
        The idea is that anyone with a Garmin account can download their .fit file and, without having to create a Marple account, 
        drop it on **Public Share Link Demo** 📊 and see what it looks like in Marple.
        
        If they like what they see and want to go a step further, they can navigate to **Ingest Garmin Data** ⌚ and push their Garmin 
        activities to analyze them in Marple.
        
        Hope you enjoy this,
        
        Arthur
        """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    st.set_page_config(page_title="Home", page_icon="🏠", layout="wide")
    st.title("About this App")

    about()
