
from time import time
import os 
import sys
from .database import Database
import json
from queue import Queue
from .database_request import DatabaseRequest
from .database_action_type import DatabaseActionType
class SQLiteEventStorage():
    """
    HIGH level api for thingsboard_gateway main loop
    """

    def __init__(self):
        self.processQueue = Queue()
        self.db = Database(self.processQueue)
        self.db.setProcessQueue(self.processQueue)
        self.db.init_table()
        self.delete_time_point = None
        self.last_read = time()
        self.stopped = False

    def get_event_pack(self):
        if not self.stopped:
            data_from_storage = self.read_data()
            try:                
                event_pack_timestamps, event_pack_messages = zip(*([(item[0],item[1]) for item in data_from_storage]))
            except ValueError as e:
                return []
            self.delete_time_point = max(event_pack_timestamps)          
            return event_pack_messages
        else:
            return []

    def event_pack_processing_done(self):
        if not self.stopped:
            self.delete_data(self.delete_time_point)

    def read_data(self):
        self.db.__stopped = True
        data = self.db.read_data()
        self.db.__stopped = False
        return data

    def delete_data(self, ts):
        return self.db.delete_data(ts)

    def put(self, message):
        try:
            if not self.stopped:
                _type = DatabaseActionType.WRITE_DATA_STORAGE
                request = DatabaseRequest(_type, message)
                self.processQueue.put(request)
                return True
            else:
                return False
        except Exception as e:
            print(e)

    def stop(self):
        self.stopped = True
        self.db.__stopped = True
        self.db.closeDB() 

    def len(self):
        
        return self.processQueue.empty()






