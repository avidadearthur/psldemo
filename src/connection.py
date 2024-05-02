import os
import streamlit as st

from marple import Marple


class Connection:
    def __init__(self):
        self.token = st.secrets["ACCESS_TOKEN"]
        self.base_url = st.secrets["API_URL"]

        self.m = Marple(access_token=self.token, api_url=self.base_url)
        self.m.check_connection()

    def upload_dataframe(self, dataframe, name, marple_folder="/sdk_data", metadata={}):
        file_name = f"{name}.csv"
        dataframe.to_csv(file_name, sep=",", index=False)
        source_id = self.m.upload_data_file(file_name, marple_folder, metadata=metadata)
        os.remove(file_name)
        return source_id
