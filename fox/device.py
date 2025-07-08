# Global imports
from datetime import datetime, timedelta

# Local imports
from data import Data
from debug import Debug

class Device:
    @staticmethod
    def list():
        data = Data("device_list")
        data.set_params({"currentPage": 1, "pageSize": 500} )
        return data.get()

    @staticmethod
    def detail(serial_number=None):
        """
        Get the device details for a specific serial number.
        If no serial number is provided, it will fetch the first device in the list.
        """
        if not serial_number:
            # Fetch the device list and get the first device's serial number
            device_list = Device.list()
            print(f"Device list: {device_list}")  # Debugging line
            if not device_list or "result" not in device_list or "data" not in device_list["result"]:
                Debug.error("Device list is empty or invalid.")
            if len(device_list["result"]["data"]) == 0:
                Debug.error("No devices found in the list.")
            serial_number = device_list["result"]["data"][0]["deviceSN"]

        data = Data("device_detail")
        data.set_params({"sn": serial_number})
        return data.get()

    @staticmethod
    def variable_get():
        data = Data("device_variable_get")
        return data.get()

    @staticmethod
    def history_query(serial_number=None):
        if not serial_number:
            device = Device.detail()
            if not device or "result" not in device or "deviceSN" not in device["result"]:
                Debug.error("Device detail is empty or invalid.")
            Debug.info(f"Device detail: {device}")
            # Get the serial number from the first device in the detail response
            serial_number = device["result"]["deviceSN"]

        data = Data("device_history_query")
        yesterday = Data.get_yesterday()
        data.set_params(
            {
                "sn": serial_number,
                "variables": [],
                "begin": yesterday.begin_time,
                "end": yesterday.end_time,
            }
        )
        return data.get()

    @staticmethod
    def report_query(serial_number=None):
        if not serial_number:
            device = Device.detail()
            if (
                not device
                or "result" not in device
                or "deviceSN" not in device["result"]
            ):
                Debug.error("Device detail is empty or invalid.")

            Debug.info(f"Device detail: {device}")
            # Get the serial number from the first device in the detail response
            serial_number = device["result"]["deviceSN"]

        data = Data("device_report_query")
        yesterday = datetime.now() - timedelta(days=1)
        data.set_params( {
            "sn": serial_number,
            "year": yesterday.year,
            "month": yesterday.month,
            "day": yesterday.day,
            "dimension": "day",
            "variables": [
                "generation",
                "feedin",
                "gridConsumption",
                "chargeEnergyToTal",
                "dischargeEnergyToTal",
            ],
        } )
        return data.get()

    @staticmethod
    def generation(serial_number=None):
        """
        Get the generation data for a specific device.
        If no serial number is provided, it will fetch the first device in the list.
        """
        if not serial_number:
            device = Device.detail()
            if (
                not device
                or "result" not in device
                or "deviceSN" not in device["result"]
            ):
                Debug.error("Device detail is empty or invalid.")

            Debug.info(f"Device detail: {device}")
            # Get the serial number from the first device in the detail response
            serial_number = device["result"]["deviceSN"]

        data = Data("device_generation")
        data.disable_cache()  # We always want the latest generation data
        data.set_params(
            {
                "sn": serial_number,
            }
        )
        return data.get()
