# Local imports
from data import Data

class Module:
    @staticmethod
    def module_list(current_page=1, page_size=10):
        data = Data("module_list")
        data.set_params({"currentPage": current_page, "pageSize": page_size})
        return data.get()
