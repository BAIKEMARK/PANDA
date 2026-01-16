"""
CRUD Package
CRUD操作包
"""
import backend.app.crud.crud_user as crud_user
import backend.app.crud.crud_course as crud_course
import backend.app.crud.crud_scenario as crud_scenario
import backend.app.crud.crud_chat as crud_chat

__all__ = [
    "crud_user",
    "crud_course",
    "crud_scenario",
    "crud_chat",
]
