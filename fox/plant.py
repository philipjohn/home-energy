# Local imports
from data import Data
from debug import Debug

class Plant:
    @staticmethod
    def plant_list(current_page=1, page_size=10):
        request_param = {"currentPage": current_page, "pageSize": page_size}
        data = Data("plant_list")
        data.set_params(request_param)
        return data.get()

    @staticmethod
    def plant_detail(plant_id=None):
        if not plant_id:
            # Fetch the plant list and get the first plant's ID
            plant_list = Plant.plant_list()
            if not plant_list or "result" not in plant_list or "data" not in plant_list["result"]:
                Debug.error("Plant list is empty or invalid.")
            if len(plant_list["result"]["data"]) == 0:
                Debug.error("No plants found in the list.")
            plant_id = plant_list["result"]["data"][0]["stationID"]

        request_param = {"id": plant_id}
        data = Data("plant_detail")
        data.set_params(request_param)
        return data.get()
