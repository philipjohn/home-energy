# Global imports
import os
import requests
import sys
from datetime import datetime, timedelta
from dotenv import load_dotenv
from requests.auth import HTTPDigestAuth

load_dotenv()
key = os.getenv("MYENERGI_API_KEY")
if not key:
    print("MYENERGI_API_KEY is not set in the environment variables.")
    exit(1)

serial_number = os.getenv("MYENERGI_SERIAL_NUMBER")
if not serial_number:
    print("MYENERGI_SERIAL_NUMBER is not set in the environment variables.")
    exit(1)

# Get the previous day in YYYY-MM-DD format
yesterday = datetime.now() - timedelta(days=1)
date = yesterday.strftime("%Y-%m-%d")

# api_url = "https://s18.myenergi.net/cgi-jstatus-Z"
api_url = f"https://s18.myenergi.net/cgi-jdayhour-Z{serial_number}-{date}"

headers = {
    "accept": "application/json",
    "content-type": "application/json",
}

auth = HTTPDigestAuth(serial_number, key)

file_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
if not os.path.exists(file_dir):
    os.makedirs(file_dir)

file_name = os.path.join(file_dir, f"dayhour_{date}.json")

response = requests.get(api_url, headers=headers, auth=auth)
if response.status_code == 200:
    data = response.json()
    # Write the data to a file
    with open(file_name, "w") as file:
        file.write(response.text)
    print(f"Data written to {file_name}")
else:
    print(f"Failed to retrieve data: {response.status_code}")
    print(response.text)
    sys.exit(1)
