import os
import requests
import streamlit as st

from marple import Marple
from garminconnect import Garmin, GarminConnectConnectionError, GarminConnectTooManyRequestsError


class GarminConnection:
    def __init__(self, username, password):
        self.username = username
        self.password = password

        self.client = Garmin(self.username, self.password)
        self.client.login()


class MarpleConnection:
    def __init__(self):
        self.token = st.secrets["ACCESS_TOKEN"]
        self.base_url = st.secrets["API_URL"]
        self.m = Marple(access_token=self.token, api_url=self.base_url)
        self.m.check_connection()

    def upload_dataframe(self, dataframe, file_name, marple_folder="/", metadata={}):
        dataframe.to_csv(file_name, sep=",", index=False)
        source_id = self.m.upload_data_file(file_name, marple_folder, metadata=metadata)
        os.remove(file_name)
        return source_id

    def create_share_link(self, dataframe, file_name, marple_folder="/", metadata={}, workbook_name="running"):
        source_id = self.upload_dataframe(dataframe, file_name, marple_folder=marple_folder, metadata=metadata)

        endpoint = "/library/share/new"
        auth_header = {"Authorization": f"Bearer {self.token}"}
        payload = {"source_ids": [source_id], "workbook_name": workbook_name, "is_public": True}

        response = requests.post(f"{self.base_url}{endpoint}", headers=auth_header, json=payload)

        if response.status_code == 200:
            share_id = response.json().get("message")
            return self.fetch_share_link(share_id)

        return ""

    def fetch_share_link(self, share_id):
        endpoint = f"/library/share/{share_id}/link"
        auth_header = {"Authorization": f"Bearer {self.token}"}

        response = requests.get(f"{self.base_url}{endpoint}", headers=auth_header)

        if response.status_code == 200:
            return response.json().get("message")

        return ""
