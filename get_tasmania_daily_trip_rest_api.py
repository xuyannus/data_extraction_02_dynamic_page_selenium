import requests
import pandas as pd

request_id = "2fd090f1-d102-46fc-891c-de50dcb4bbd2"
vistor_id = "dOR1cEcmR1MnbMST8DvX-"


def get_headers():
    headers = {
        'accept': "application/json, text/plain, */*",
        'accept-currency': "AUD",
        'accept-language': "en-GB",
        'authority': "travelers-api.getyourguide.com",
        'request-id': request_id,
        'visitor-id': vistor_id,
        'visitor-platform': 'desktop',
        'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36"
    }
    return headers


def extract_daily_trip_api_helper(offset=0):
    url = f"https://travelers-api.getyourguide.com/search/v2/search?q=Tasmania&locations=209&categories=172&offset={offset}&size=60&searchSource=4"
    response = requests.request("GET", url, headers=get_headers())
    response_data = response.json()
    activity_df = pd.DataFrame(response_data['items'])
    selected_columns = ['id', 'title', 'type', 'price', 'duration', 'url']
    activity_df[selected_columns].to_csv("./tasmania_daily_trips_api.csv", index=False)


if __name__ == "__main__":
    extract_daily_trip_api_helper()
