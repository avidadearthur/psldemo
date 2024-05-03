import os
import requests
import streamlit as st
import zipfile
import tempfile

from marple import Marple
from utils import process_fit_file
from garminconnect import (
    Garmin,
    GarminConnectConnectionError,
    GarminConnectTooManyRequestsError,
)


class GarminConnection:
    def __init__(self, username, password):
        self.username = username
        self.password = password

        try:
            self.client = Garmin(self.username, self.password)
            self.client.login()
        except (GarminConnectConnectionError, GarminConnectTooManyRequestsError) as e:
            print(f"Failed to connect to Garmin: {e}")
            raise ConnectionError("Could not connect to Garmin Connect")

    def get_garmin_activities(self, amount):
        try:
            activities = self.client.get_activities(0, amount)
            activities_dict = {}

            for activity in activities:
                activity_id = activity["activityId"]
                fit_data = self.client.download_activity(activity_id, dl_fmt=Garmin.ActivityDownloadFormat.ORIGINAL)

                with tempfile.TemporaryDirectory() as temp_dir:
                    zip_path = os.path.join(temp_dir, f"{activity_id}.zip")
                    fit_path = os.path.join(temp_dir, f"{activity_id}_ACTIVITY.fit")

                    with open(zip_path, "wb") as file:
                        file.write(fit_data)

                    with zipfile.ZipFile(zip_path, "r") as zip_ref:
                        zip_ref.extractall(temp_dir)

                    if os.path.exists(fit_path):
                        activities_dict[activity_id] = process_fit_file(fit_path)
                    else:
                        print(f"Expected FIT file not found: {fit_path}")

            return activities_dict

        except Exception as e:
            print(f"Error fetching activities: {e}")
            return {}


class MarpleConnection:
    def __init__(self, token=None):
        self.token = st.secrets["ACCESS_TOKEN"] if not token else token
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
