# Global imports
import hashlib
import os
import requests
import time
from dotenv import load_dotenv

# Local imports
from debug import Debug

class API:

    _api_prefix = "/op/v0/"
    _domain = None
    _endpoint = None
    _key = None
    _method = "get"
    _params = None

    def __init__(self):
        """
        Initialize the API class.
        """

        load_dotenv()
        self._key = os.getenv("FOX_API_KEY")
        self._domain = os.getenv("FOX_API_DOMAIN", "https://www.foxesscloud.com")

        # Bail if the key or domain is not set
        if not self._key or not self._domain:
            Debug.error(
                "FOX_API_KEY and FOX_API_DOMAIN must be set in the environment variables."
            )

    def get_url(self):
        """
        Get the full URL for the API request.
        :return: The full URL as a string.
        """
        if not self._endpoint:
            Debug.error("API endpoint is not set. Use set_name() to specify the endpoint.")

        return f"{self._domain}{self._api_prefix}{self._endpoint}"

    def get_headers(self):
        """
        This function is used to generate the headers for the API request.
        :return: with authentication header
        """
        timestamp = round(time.time() * 1000)
        path = self._api_prefix + self._endpoint
        Debug.info(f"Generating signature with path: {path}, key: {self._key}, timestamp: {timestamp}")
        signature = fr'{path}\r\n{self._key}\r\n{timestamp}'
        Debug.info(f"Signature text: {signature}")
        result = {
            'token': self._key,
            'lang': 'en',
            'timestamp': str(timestamp),
            'signature': self.md5c(text=signature),
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/117.0.0.0 Safari/537.36'
        }
        Debug.info(f"Generated headers: {result}")
        return result

    def md5c(self, text="", _type="lower"):
        res = hashlib.md5(text.encode(encoding="UTF-8")).hexdigest()
        if _type == "lower":
            return res
        else:
            return res.upper()

    def send_request(self):
        url = self.get_url()
        Debug.info(f"Requesting {url} with method {self._method} and params {self._params}")
        if self._method == "get":
            response = requests.get(
                url=url,
                params=self._params,
                headers=self.get_headers(),
                verify=False
            )
        elif self._method == "post":
            response = requests.post(
                url=url,
                json=self._params,
                headers=self.get_headers(),
                verify=False
            )
        else:
            Debug.error(f"Invalid request method: {self._method}. Use 'get' or 'post'.")

        return response

    def set_name(self, name):
        """
        Set the data name for the API.
        :param name: The name of the data to be set.
        """
        if not name:
            Debug.error("Data name cannot be empty.")

        match name:
            case "device_list":
                self._endpoint = "device/list"
                self._method = "post"
            case "device_detail":
                self._endpoint = "device/detail"
                self._method = "get"
            case "device_variable_get":
                self._endpoint = "device/variable/get"
                self._method = "get"
            case "device_history_query":
                self._endpoint = "device/history/query"
                self._method = "post"
            case "device_report_query":
                self._endpoint = "device/report/query"
                self._method = "post"
            case "device_generation":
                self._endpoint = "device/generation"
                self._method = "get"
            case "module_list":
                self._endpoint = "module/list"
                self._method = "post"
            case "plant_list":
                self._endpoint = "plant/list"
                self._method = "post"
            case "plant_detail":
                self._endpoint = "plant/detail"
                self._method = "get"
            case "user_get_access_count":
                self._endpoint = "user/getAccessCount"
                self._method = "get"
            case _:
                Debug.error(f"Invalid data name: {name}.")

    def set_params(self, params):
        """
        Set the parameters for the API request.
        :param params: A dictionary containing the parameters.
        """
        self._params = params
