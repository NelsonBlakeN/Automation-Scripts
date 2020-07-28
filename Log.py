"""
Log interface:
* Write info
* Write warning
* Write error
* Define source (text/database/cloud service/etc)
* Log interface won't have a source, and it will be up to the subclasses to determine
  where the messages are sent and how. But any user or factory can instantiate any ILog
  and call log.info and trust that it goes to the right place
* In theory, it would be good to have a BaseLog class, for at least having a common
  base constructor that took in the name of the log. From here, child Log classes could
  define anything else they wanted in their constructor (like a text file path), as long
  as it still included a name for the log. But this is Python, and types don't have to be
  that strict.
"""

import abc
import os
import logging


class ILog(metaclass=abc.ABCMeta):
    """
    Log interface
    """

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'info') and
                callable(subclass.info))

    @abc.abstractmethod
    def info(self, message: str):
        """Write an information message to the log"""
        raise NotImplementedError

    @abc.abstractmethod
    def warning(self, message: str):
        """Write a warning message to the log"""
        raise NotImplementedError

    @abc.abstractmethod
    def _verify_log_location(self, location: str):
        """Verify that the location of the log is valid"""
        raise NotImplementedError


class TextLog(ILog):
    '''Creates a log as a text file'''

    def __init__(self, log_name: str, log_path: str = None):
        '''
        Instantiates an instance of the TextLog, a text file based log.
        :param log_name: The name of the log file.
        :param log_path: The location of the log file, not including the name.
        '''

        if not log_path:
            return

        # Verify path
        self.__verify_log_location(log_path)

        # Create logger
        self.log = logging.getLogger(log_name)
        self.log.setLevel(logging.INFO)

        # Create handler and set level
        handler = logging.FileHandler(log_path + log_name)
        handler.setLevel(logging.INFO)

        # Create formatter
        formatter = logging.Formatter('%(asctime)s : %(name)s : %(levelname)s : %(message)s')

        # Add formatter to handler
        handler.setFormatter(formatter)

        # Add handler to logger
        self.log.addHandler(handler)

    def info(self, message: str):
        """
        Overrides ILog.info
        Writes an information message to the log
        :param message: The message to be written
        """
        self.log.info(message)

    def warning(self, message: str):
        """Overrides ILog.warning"""
        self.log.warning(message)

    def _verify_log_location(self, location):
        """
        Overrides ILog.__verify
        Verify if the location of the given file exists.
        If the location does not exist, it will be created recursively.
        :param path: The given path of the file, not including the name of the file.
        """
        items = location.split("/")
        folder_path = os.path.expanduser(items.pop(0) + '/')
        for item in items:
            folder_path += item + "/"
            if not os.path.exists(folder_path):
                os.mkdir(folder_path)


class DbLog(ILog):
    '''Creates a log as a database'''

    def info(self, message: str):
        '''Overrides ILog.info'''
        pass

    def warning(self, message: str):
        '''Overrides ILog.warning'''
        pass
