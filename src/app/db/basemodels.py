from enum import Enum

from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, declared_attr


class Base(AsyncAttrs, DeclarativeBase):
    """Абстрактный базовый класс для создания таблиц."""

    __abstract__ = True

    @declared_attr
    def __tablename__(cls):
        """Использование названий таблиц из названий класса."""
        return cls.__name__.lower()

    def to_dict(self):
        """Функция ковертации модели в словарь."""
        return {
            field.name: (
                getattr(self, field.name).value
                if isinstance(getattr(self, field.name), Enum)
                else getattr(self, field.name)
            )
            for field in self.__table__.c
        }
