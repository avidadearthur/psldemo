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