import streamlit as st
import pandas as pd


def ingest_data():
    st.write("Here you can upload your data and quickly get a shareable link with a nice plot of it!")

    file = st.file_uploader("Choose a CSV file", type=["csv"])

    if file and st.button("Ingest"):
        content = file.read().decode("utf-8")
        print(content)


if __name__ == "__main__":
    st.set_page_config(page_title="PSL Demo", page_icon="📊", layout="wide")
    st.title("Public Share Link Demo")
    ingest_data()
