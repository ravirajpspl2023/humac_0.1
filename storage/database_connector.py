
import sqlite3
from sqlite3 import connect, Connection
from threading import RLock
from typing import Optional

from os.path import exists

class DatabaseConnector:
    def __init__(self, settings):
        self.data_file_path = './database.db'
        self.connection: Optional[Connection] = None
        self.lock = RLock()

    def connect(self):
        """
        Create database file in path from settings
        """
        try:
            self.connection = connect(self.data_file_path, check_same_thread=False)
        except Exception as e:
            print(e)

    def commit(self):
        """
        Commit changes
        """

        try:
            with self.lock:
                self.connection.commit()

        except Exception as e:
            print(e)

    def execute(self, *args):
        """
        Execute changes
        """
        # log.debug("Execute %s to DB", str(args))
        try:
            with self.lock:
                return self.connection.execute(*args)
        except sqlite3.ProgrammingError:
            pass
        except Exception as e:
            print(e)

    def rollback(self):
        """
        Rollback changes after exception
        """
        try:
            with self.lock:
                self.connection.rollback()

        except Exception as e:
            print(e)

    def close(self):
        """
        Closes database file
        """
        try:
            with self.lock:
                self.connection.close()

        except Exception as e:
            print(e)

    def get_cursor(self):
        try:
            return self.connection.cursor()

        except Exception as e:
            print(e)
