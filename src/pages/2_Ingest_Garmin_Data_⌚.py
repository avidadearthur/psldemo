import streamlit as st
from connection import MarpleConnection, GarminConnection


def ingest_data():
    st.markdown(
        """
        Link your Garmin credentials and your Marple workspace token to push activity data to Marple!

        Your Marple Workspace Token needs to be manually generated if you don't have one, go to Settings > Tokens > Add Token. 
        """,
            unsafe_allow_html=True,
        )

    if "garmin" not in st.session_state or "marple" not in st.session_state:
        st.session_state.garmin = None
        st.session_state.marple = None

    with st.expander("Garmin and Marple Settings"):
        garmin_username = st.text_input("Garmin Username", key="garmin_username")
        garmin_password = st.text_input("Garmin Password", type="password", key="garmin_password")
        marple_token = st.text_input("Marple Workspace Token", key="marple_token")

        link_button = st.button("Link")

        if link_button:
            try:
                st.session_state.garmin = GarminConnection(garmin_username, garmin_password)
                st.session_state.marple = MarpleConnection(marple_token)
                st.success("Successfully linked Garmin and Marple accounts!")
            except Exception as e:
                st.error(f"Failed to link accounts: {str(e)}")
                return

    if st.session_state.garmin and st.session_state.marple:
        with st.form(key="num_activities"):
            num_activities = st.number_input("Enter the number of activities to upload:", min_value=1, value=5)
            submit_button = st.form_submit_button(label="Send to Marple")

            if submit_button:
                try:
                    existing_files = st.session_state.marple.get_content(path="/garmin_activities")
                    existing_files = [file["path"].lower() for file in existing_files["message"]]

                    activities_info = st.session_state.garmin.get_garmin_activities(num_activities)
                    skipped_files = []
                    uploaded_count = 0

                    for activity_id, (df, activity_type) in activities_info.items():
                        file_name = f"activity_{activity_id}_{activity_type}.csv"
                        full_path = f"garmin_activities/{file_name}".lower()

                        if full_path in existing_files:
                            skipped_files.append(file_name)
                            continue

                        metadata = {"activity_id": activity_id, "activity_type": activity_type}
                        upload_message = st.empty()
                        upload_message.write("Uploading data to Marple...")
                        source_id = st.session_state.marple.upload_dataframe(
                            df, file_name, "/garmin_activities", metadata
                        )
                        upload_message.write(f"Uploaded {source_id} successfully.")
                        upload_message.empty()
                        uploaded_count += 1

                    if skipped_files:
                        st.info(
                            f"Skipped uploading the following files as they already exist: {', '.join(skipped_files)}"
                        )
                    message = f"Successfully uploaded {uploaded_count} out of {num_activities} requested activities to Marple."

                    if uploaded_count != num_activities:
                        st.warning(message)
                    elif uploaded_count == num_activities:
                        st.success(message)

                except Exception as e:
                    st.error(f"Error during activity upload: {str(e)}")


if __name__ == "__main__":
    st.set_page_config(page_title="Ingest Garmin Data", page_icon="⌚", layout="wide")
    st.title("Ingest Garmin Data")

    ingest_data()
