# Global imports
import sys
import urllib3

# Local imports
from debug import Debug
from device import Device
from module import Module
from plant import Plant
from user import User

urllib3.disable_warnings()

if __name__ == '__main__':
    # Get the function to execute from the command line arguments
    if len(sys.argv) > 1:
        data_name = sys.argv[1]
        args = sys.argv[2:] if len(sys.argv) > 2 else None

        match data_name:

            case "device_list":
                Debug.info("Fetching device list...")
                Device.list()

            case "device_detail":
                serial_number = args[0] if args else None
                Debug.info(f"Fetching device detail for serial number: {serial_number}")
                Device.detail(serial_number)

            case "device_variable_get":
                Debug.info("Fetching device variables...")
                Device.variable_get()

            case "device_history_query":
                serial_number = args[0] if args else None
                Debug.info("Fetching device history query...")
                Device.history_query(serial_number)

            case "device_report_query":
                serial_number = args[0] if args else None
                Debug.info("Fetching device report query...")
                Device.report_query(serial_number)

            case "device_generation":
                serial_number = args[0] if args else None
                Debug.info("Fetching device generation...")
                Device.generation(serial_number)
                
            case "module_list":
                current_page = int(args[0]) if args and len(args) > 0 else 1
                page_size = int(args[1]) if args and len(args) > 1 else 10
                Debug.info("Fetching module list...")
                Module.module_list(current_page=current_page, page_size=page_size)

            case "plant_list":
                current_page = int(args[0]) if args and len(args) > 0 else 1
                page_size = int(args[1]) if args and len(args) > 1 else 10
                Debug.info("Fetching plant list...")
                Plant.plant_list(current_page=current_page, page_size=page_size)
                
            case "plant_detail":
                plant_id = args[0] if args else None
                if plant_id:
                    Debug.info(f"Fetching plant detail for plant ID: {plant_id}")
                else:
                    Debug.info("Fetching plant detail for the first plant in the list.")
                    
                Plant.plant_detail(plant_id)
                
            case "user_get_access_count":
                Debug.info("Fetching user access count...")
                User.user_get_access_count()

            case _:
                Debug.error(f"Invalid data name: {data_name}.")
    else:
        Debug.warning("Usage: python example.py <data_name> [<args>]")
        Debug.warning("Example: python index.py device_detail 123456789")
