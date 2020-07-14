import os
import logging


class Logger(object):
    def __init__(self, log_name=None):
        self.logs = []
        if log_name:
            self.LOG_NAME = log_name
            self.add_log(self.LOG_NAME)

    def log(self, message):
        for log in self.logs:
            log.info(message)

    def error(self, message):
        for log in self.logs:
            log.error(message)

    def warning(self, message):
        for log in self.logs:
            log.warning(message)

    def add_log(self, name):
        """
        Add a new log object for tracking and writing.
        """
        if not name:
            raise Exception("Filename is required.")

        # Verify that log location is available
        # before creating the log config
        self.__verify_log_location(name)
        log = self.__create_log(name.split(".")[0], name)
        self.logs.append(log)

    def __verify_log_location(self, file_path):
        """
        Verify if the location of the given file exists.
        If the location does not exist, it will be created recursively.
        """
        items: list = file_path.split("/")
        items.pop(-1)
        folder_path = os.path.expanduser(items.pop(0) + '/')
        for item in items:
            folder_path += item + "/"
            if not os.path.exists(folder_path):
                os.mkdir(folder_path)

    def __create_log(self, name, logfile, default_level=logging.INFO):
        """
        Creates a log using the given name, location, and level
        TODO: Utilize a factory that generates the right type of log (text file, database, cloud, etc)
        """

        handler = logging.Handler(logfile)
        # TODO: Create custom formatter

        log = logging.getLogger(name)
        log.setLevel(default_level)
        log.addHandler(handler)

        return log
