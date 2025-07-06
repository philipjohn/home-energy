# Global imports
import json
import os
import requests
import sys
import time
from collections import namedtuple
from datetime import datetime, timedelta
from dotenv import load_dotenv
from json import JSONDecodeError

# Local imports
from api import API
from debug import Debug

class Data:

    args = None
    cache = True
    data_dir = None
    name = None

    # Specify the list of valid data names
    valid_data_names = [
        'device_list',
        'device_detail',
        'device_variable_get',
        'device_history_query',
        'device_report_query',
        'device_generation',
        'module_list',
        'plant_list',
        'plant_detail',
        'user_get_access_count',
    ]

    def __init__(self, name=None, args=None):
        # Load environment variables from .env file
        load_dotenv()

        # Get the directory for saving data
        self.data_dir = os.getenv(
            "FOX_DATA_DIR", os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
        )

        # Ensure we have a name to work with
        if not name:
            Debug.error("Data name cannot be empty.")
            return

        # Validate the data name
        if not self.is_valid_data_name(name):
            Debug.error(f"Invalid data name: {name}. Valid names are: {', '.join(self.valid_data_names)}")
            return

        # Set the name and args
        self.name = name
        self.args = args if args else {}

    def disable_cache(self):
        """
        Disable caching for the data retrieval.
        """
        self.cache = False
        Debug.warning(f"Cache disabled for {self.name}")

    def fetch_data(self):
        """
        Fetch the data from the API.
        :return: The response from the API as a dictionary.
        """
        Debug.info(f"Fetching data for {self.name}")

        # Create an API instance
        api = API()
        api.set_name(self.name)
        if self.args:
            api.set_params(self.args)
        try:
            response = api.send_request()
        except requests.exceptions.RequestException as e:
            Debug.error(f"Request failed: {e}")
            return None

        self.save_response_data(response.json())

        return response.json() if response else None

    def get(self):
        """
        Get the specified data, checking first if it exists in the data directory.
        """
        Debug.info(f"Getting data for {self.name}")
        Debug.info(f"Cache enabled: {self.cache}")
        if self.cache and self.has_saved_data():
            Debug.info(f"Using existing data for {self.name}")
            return self.get_saved_data()

        return self.fetch_data()

    def get_file_name(self):
        """
        Get the file name for the specified data.
        :return: The file name as a string.
        """
        file_name = self.name
        match self.name:
            # Add the serial number to the file name.
            case "device_detail" | "device_generation":
                if "sn" in self.args:
                    file_name = f"{self.name}_{self.args['sn']}"

            # Add the serial number and date to the file name.
            case "device_history_query":
                file_name = "_".join(
                    [
                        self.name,
                        self.args.get("sn"),
                        datetime.fromtimestamp(
                            self.args.get("begin", 0) / 1000
                        ).strftime("%Y-%m-%d"),
                    ]
                )

            # Add the serial number and date to the file name.
            case "device_report_query":
                date_part = datetime.strptime(
                    "-".join(
                        [
                            str(self.args.get("year")),
                            str(self.args.get("month")),
                            str(self.args.get("day")),
                        ]
                    ),
                    "%Y-%m-%d"
                ).strftime("%Y-%m-%d")
                file_name = '_'.join(
                    [
                        self.name,
                        self.args.get("sn", "unknown"),
                        date_part,
                    ]
                )

            # Add the module ID to the file name.
            case "plant_detail":
                if "id" in self.args:
                    file_name = f"{self.name}_{self.args['id']}"

        return file_name + ".json"

    def get_saved_data(self):
        """
        Get the saved data from the specified file in the data directory.
        :param name: The name of the file to read (without the 'data/' prefix).
        :return: The content of the file as a dictionary.
        """
        file_path = os.path.join(self.data_dir, self.get_file_name())
        contents = open(file_path, "r", encoding="utf-8")
        parsed = json.load(contents)
        contents.close()
        return parsed["response"]

    @staticmethod
    def get_yesterday():
        """
        Get the begin and end time of yesterday in milliseconds.
        :return: a named tuple with begin_time and end_time
        """
        now = datetime.now()
        today_tup = (
            now.year,
            now.month,
            now.day,
            0,
            0,
            0,
            now.weekday(),
            now.timetuple().tm_yday,
            now.timetuple().tm_isdst,
        )
        today = time.mktime(today_tup)
        yesterday = today - 86400  # 24 hours before today
        begin_time = int(yesterday * 1000)  # Convert to milliseconds
        end_time = begin_time + 86399999  # 24 hours in milliseconds minus 1 millisecond
        file_string = datetime.fromtimestamp(begin_time / 1000).strftime("%Y-%m-%d")
        return namedtuple("Time", ["begin_time", "end_time", "file_string"])(
            begin_time, end_time, file_string
        )

    def has_saved_data(self):
        """
        Check if the specified data file exists in the data directory.
        :param name: The name of the file to check (without the 'data/' prefix).
        :return: True if the file exists, False otherwise.
        """
        file_path = os.path.join(self.data_dir, self.get_file_name())
        Debug.info(f"Checking if data file exists: {file_path}")
        return os.path.exists(file_path)

    def is_valid_data_name(self,name):
        """
        Check if the provided name is a valid data file name.
        :param name: The name of the file to check (without the 'data/' prefix).
        :return: True if the name is valid, False otherwise.
        """

        # Check if the name is in the list of valid data names
        if name in self.valid_data_names:
            return True
        else:
            Debug.error(f"Invalid data name: {name}. Valid names are: {', '.join(self.valid_data_names)}")
            return False

    def save_response_data(self, response):
        """
        Save the response data to a file in the data directory.
        :param response: The response from the API as a dictionary.
        """
        file = self.get_file_name()
        file_path = os.path.join(self.data_dir, file)
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump({"response": response}, f, ensure_ascii=False, indent=4)
            Debug.info(f"Data saved to {file_path}")
        except (IOError, JSONDecodeError) as e:
            Debug.error(f"Failed to save data to {file_path}: {e}")
            return None

    def set_params(self, params):
        """
        Set the parameters for the API request.
        :param params: A dictionary containing the parameters.
        """
        self.args = params
        Debug.info(f"Parameters set for {self.name}: {self.args}")
