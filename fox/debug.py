# Global imports
import os
import sys
from dotenv import load_dotenv

class Debug:
    @staticmethod
    def on():
        """
        Print debug information if debug mode is enabled.
        """
        load_dotenv()
        return os.getenv("DEBUG", "False").lower() in ("true", "1", "yes")
            
    @staticmethod
    def info(message):
        """
        Print an informational message.
        :param message: The informational message to print.
        """
        if Debug.on():
            print(f"INFO: {message}")

    @staticmethod
    def warning(message):
        """
        Print a warning message.
        :param message: The warning message to print.
        """
        if Debug.on():
            print(f"WARNING: {message}")

    @staticmethod
    def error(message):
        """
        Print an error message and exit the program.
        :param message: The error message to print.
        """
        if Debug.on():
            print(f"ERROR: {message}")

        sys.exit(1)
