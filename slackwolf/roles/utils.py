import importlib

from .types import RoleTypes


def get_role_class(role: RoleTypes):
    mod = importlib.import_module('slackwolf.roles')
    role_class = getattr(mod, role.value)
    return role_class
