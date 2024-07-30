from nestipy_alchemy import SqlAlchemyPydanticMapper
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass
from strawberry_sqlalchemy_mapper import StrawberrySQLAlchemyMapper

s_sq_mapper = StrawberrySQLAlchemyMapper()
p_sq_mapper = SqlAlchemyPydanticMapper()


class Base(DeclarativeBase, MappedAsDataclass):
    pass
