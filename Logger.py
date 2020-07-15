import os
import logging
from Log import TextLog

class Logger(object):
    def __init__(self, log_name=None, log_type:str=None):
        self.logs = []
        if log_name:
            self.LOG_NAME = log_name
            self.add_log(self.LOG_NAME, log_type)

    def log(self, message):
        for log in self.logs:
            log.info(message)

    def error(self, message):
        for log in self.logs:
            log.error(message)

    def warning(self, message):
        for log in self.logs:
            log.warning(message)

    def add_log(self, name: str, log_type: str, log_location: str=None):
        """
        Add a new log object for tracking and writing.
        """
        if not name:
            raise Exception("Log name is required.")
        if not log_type:
            raise Exception("Log type is required.")

        # Verify that log location is available
        # before creating the log config
        print(TextLog)
        log = TextLog(name, log_location)
        self.logs.append(log)
