import io
import pandas as pd
import streamlit as st
from fitparse import FitFile
from connection import Connection
from utils import process_location_columns


def get_public_share_link(conn, df, file_name):
    return conn.create_share_link(dataframe=df, file_name=file_name)


def process_fit_file(file):
    fitfile = FitFile(file)
    records = []

    for record in fitfile.get_messages("record"):
        record_data = {data.name: data.value for data in record}
        records.append(record_data)

    df = pd.DataFrame(records)
    df = df[[col for col in df.columns if not col.startswith("unknown_")]]
    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True).astype("int64") / 10**9
    df = process_location_columns(df)
    df.columns = df.columns.str.replace("_", " ", regex=False)
    return df


def ingest_data(conn):
    st.write("Upload your exercising data and quickly get a shareable link with nice visualizations!")

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

    conn = Connection()
    ingest_data(conn)
