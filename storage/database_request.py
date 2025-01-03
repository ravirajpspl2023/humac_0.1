from .database_action_type import DatabaseActionType


class DatabaseRequest:

    def __init__(self, _type: DatabaseActionType, data):
        self.type = _type
        self.data = data