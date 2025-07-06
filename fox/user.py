# Local imports
from data import Data

class User:
    @staticmethod
    def user_get_access_count():
        data = Data("user_get_access_count")
        return data.get()
