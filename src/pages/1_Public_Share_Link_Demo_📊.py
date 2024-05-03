import io
import pandas as pd
import streamlit as st
from connection import MarpleConnection
from utils import process_fit_file


def get_public_share_link(conn, df, file_name):
    return conn.create_share_link(dataframe=df, file_name=file_name)


def ingest_data(conn):
    st.markdown(
        """
    A public sharing link can be used to share your visualization view with people outside of your workspace,
    or even without a Marple account.

    Upload your exercising data and quickly get a shareable link with nice visualizations!
    """,
        unsafe_allow_html=True,
    )

    preview_toggle = st.checkbox("Show preview")

    file = st.file_uploader("Add your file here", type=["csv", "fit"])

    if file:
        if file.name.endswith(".csv"):
            df = pd.read.csv(io.StringIO(file.read().decode("utf-8")))
        elif file.name.endswith(".fit"):
            df = process_fit_file(file)

        if preview_toggle:
            st.dataframe(df.head(50), use_container_width=True)

        if st.button("Upload to Marple"):
            upload_message = st.empty()
            upload_message.write("Uploading data to Marple...")

            psl_url = get_public_share_link(conn, df, file.name)

            upload_message.empty()
            st.write(f"Here's your PSL: {psl_url}")


if __name__ == "__main__":
    st.set_page_config(page_title="PSL Demo", page_icon="📊", layout="wide")
    st.title("Public Share Link Demo")

    conn = MarpleConnection()
    ingest_data(conn)
