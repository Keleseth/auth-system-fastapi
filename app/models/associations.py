"""
Модель ассоциации между пользователями и ролями.
"""
from sqlalchemy import Table, Column, ForeignKey, Integer
from sqlalchemy import UUID as SQUUID

from .base import BaseModel


user_role_association = Table(
    'user_role_association',
    BaseModel.metadata,
    Column(
        'user_id',
        SQUUID,
        ForeignKey('user_model.id', ondelete='CASCADE'),
        primary_key=True,
    ),
    Column(
        'role_id',
        Integer,
        ForeignKey('role_model.id', ondelete='CASCADE'),
        primary_key=True,
    ),
)
