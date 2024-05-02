import os
import requests
import streamlit as st

from marple import Marple


class Connection:
    def __init__(self):
        self.token = st.secrets["ACCESS_TOKEN"]
        self.base_url = st.secrets["API_URL"]

        self.m = Marple(access_token=self.token, api_url=self.base_url)
        self.m.check_connection()

    def upload_dataframe(self, dataframe, name, marple_folder="/", metadata={}):
        # upload data
        file_name = f"{name}.csv"
        dataframe.to_csv(file_name, sep=",", index=False)
        source_id = self.m.upload_data_file(file_name, marple_folder, metadata=metadata)
        os.remove(file_name)

        # create sharelink
        psl_url = ''

        endpoint = "/library/share/new"
        auth_header = {"Authorization": f"Bearer {self.token}"}
        # to-do: make workbook_name a var that changes depending on what's selected in the Streamlit app
        payload = {"source_ids": [source_id], "workbook_name": "running", "is_public": True}

        response = requests.post(f"{self.base_url}{endpoint}", headers=auth_header, json=payload)

        if response.status_code == 200:
            # fetch url 
            share_id = response.json().get("message")
            endpoint = f"/library/share/{share_id}/link"

            response = requests.get(f"{self.base_url}{endpoint}", headers=auth_header, json=payload)

            if response.status_code == 200:
                psl_url = response.json().get("message")

        return psl_url
