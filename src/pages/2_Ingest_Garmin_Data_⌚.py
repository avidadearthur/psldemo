import streamlit as st
from connection import MarpleConnection, GarminConnection


def ingest_data():
    st.write("Link your Garmin credentials and your Marple workspace token to push activity data to Marple!")

    with st.expander("Garmin and Marple Settings"):
        garmin_username = st.text_input("Garmin Username")
        garmin_password = st.text_input("Garmin Password", type="password")
        marple_token = st.text_input("Marple Workspace Token")

        link_button = st.button("Link")

        if link_button:
            try:
                garmin = GarminConnection(garmin_username, garmin_password)
                marple = MarpleConnection(marple_token)
                st.success("Successfully linked Garmin and Marple accounts!")
                link_button = False
            except Exception as e:
                st.error(f"Failed to link accounts: {str(e)}")

    with st.form(key="num_activities"):
        num_activities = st.number_input("Enter the number of activities to upload:", min_value=1, value=5)
        submit_button = st.form_submit_button(label="Send to Marple")

        if submit_button:
            # This is a placeholder for actual activity uploading
            st.success(f"Successfully scheduled upload of {num_activities} activities to Marple.")


if __name__ == "__main__":
    st.set_page_config(page_title="Ingest Garmin Data", page_icon="⌚", layout="wide")
    st.title("Ingest Garmin Data")

    conn = MarpleConnection()
    ingest_data()
