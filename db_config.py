from enum import Enum

host = 'host'
user = 'user'
password = 'password'
db_name = 'group'


class States(Enum):
    S_START = 0
    S_FACULTY = 1
    S_GROUP_CLASS = 2
    S_GROUP_NAME = 3
    S_SCHEDULE = 4