"""
CRUD Package
CRUD操作包
"""
import crud.crud_user as crud_user
import crud.crud_course as crud_course
import crud.crud_scenario as crud_scenario
import crud.crud_chat as crud_chat

__all__ = [
    "crud_user",
    "crud_course",
    "crud_scenario",
    "crud_chat",
]
