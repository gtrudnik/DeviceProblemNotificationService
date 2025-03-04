from enum import Enum


class Roles(str, Enum):
    super_admin = "super_admin"
    admin = 'admin'
    user = 'user'
    banned = 'banned'
