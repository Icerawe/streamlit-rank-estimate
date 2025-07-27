import requests
import pandas as pd


def get_sheet_data(api_key, spreadsheet_id, sheet_name):
    """Fetch data from a specific sheet."""
    url = (
        f"https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}/values/{sheet_name}"
        f"?key={api_key}"
    )
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"API request failed: {response.text}")

    data = response.json().get("values", [])
    if not data:
        return pd.DataFrame()  # Return empty DataFrame if no data

    # Normalize data to match the header length
    max_cols = len(data[0])
    normalized_data = [row + [''] * (max_cols - len(row)) for row in data]
    return pd.DataFrame(normalized_data[1:], columns=normalized_data[0])