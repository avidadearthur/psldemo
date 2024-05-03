import pandas as pd
from fitparse import FitFile


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
