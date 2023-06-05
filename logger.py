from datetime import datetime
import logging
import sys
import traceback


class Logger:

    @staticmethod
    def prepend_time(text):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return f"[{timestamp}] {text}"

    def __init__(self, file_path):
        self.file_path = file_path
        logging.basicConfig(filename=self.file_path, level=logging.INFO)

    def i(self, text):
        text = Logger.prepend_time(text)
        print(text)
        logging.info(text)

    def w(self, text):
        text = Logger.prepend_time(text)
        print(f'\033[93m{text}\033[0m')
        logging.warning(text)

    def e(self, text=None, error=None):
        if text:
            text = Logger.prepend_time(text)
            print(f'\033[91m{text}\033[0m')
            logging.error(text, exc_info=error)

        if error:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            error_string = traceback.format_exception(exc_type, exc_value, exc_traceback)
            error_trace = "".join(error_string)
            text = Logger.prepend_time(error_trace)
            print(f'\033[91m{text}\033[0m')
            logging.error(text)

logger = Logger('bot.log')
