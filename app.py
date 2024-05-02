import streamlit as st
import pandas as pd
import io
from fitparse import FitFile


def upload_to_marple(df):
    st.write("Uploading data to Marple...")


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


def process_location_columns(df, columns=None):
    if columns is None:
        columns = [c for c in df.columns if c.endswith("_lat") or c.endswith("_long")]
    else:
        columns = [c for c in columns if c in df.columns]

    for column in columns:
        df[column] = semicircles_to_degrees(df[column])

    return df


def semicircles_to_degrees(semicircles):
    return semicircles * (180 / (2**31))


def ingest_data():
    st.write("Here you can upload your data and quickly get a shareable link with a nice plot of it!")

    file = st.file_uploader("Choose a file", type=["csv", "fit"])

    if file:
        if file.name.endswith(".csv"):
            df = pd.read_csv(io.StringIO(file.read().decode("utf-8")))
        elif file.name.endswith(".fit"):
            df = process_fit_file(file)

        st.write("Preview of the first 50 rows:")
        st.dataframe(df.head(50), use_container_width=True)

        if st.button("Upload to Marple"):
            upload_to_marple(df)


if __name__ == "__main__":
    st.set_page_config(page_title="PSL Demo", page_icon="📊", layout="wide")
    st.title("Public Share Link Demo")
    ingest_data()
