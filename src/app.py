import io
import pandas as pd
import streamlit as st


from fitparse import FitFile
from connection import Connection
from utils import process_location_columns


def upload_to_marple(conn, df):
    st.write("Uploading data to Marple...")

    psl_url = conn.upload_dataframe(df, name="exercise_data")

    st.write(f"{psl_url}")


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

    return df


def ingest_data(conn):
    st.write("Upload your exercising data and quickly get a shareable link with nice visualizations!")

    file = st.file_uploader("", type=["csv", "fit"])

    if file:
        if file.name.endswith(".csv"):
            df = pd.read_csv(io.StringIO(file.read().decode("utf-8")))
        elif file.name.endswith(".fit"):
            df = process_fit_file(file)

        st.write("Preview of the first 50 rows:")
        st.dataframe(df.head(50), use_container_width=True)

        if st.button("Upload to Marple"):
            upload_to_marple(conn, df)


if __name__ == "__main__":
    st.set_page_config(page_title="PSL Demo", page_icon="📊", layout="wide")
    st.title("Public Share Link Demo")

    conn = Connection()
    ingest_data(conn)
