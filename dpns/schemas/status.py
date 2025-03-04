from enum import Enum


class Status(str, Enum):
    active = "active"
    resolved = 'resolved'