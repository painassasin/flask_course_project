from typing import List, Type

from marshmallow import Schema
from sqlalchemy.orm.scoping import scoped_session

from project.dao import BaseDAO
from project.tools.exceptions import ItemNotFoundException
from project.tools.schemas import BaseSchema
from project.utils.utils import get_limit_and_offset


class BaseService:
    def __init__(self, session: scoped_session):
        self._db_session = session


class ItemServiceBase(BaseService):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dao: BaseDAO = NotImplemented
        self.schema: Schema = BaseSchema
        self.not_found_exception: Type[ItemNotFoundException] = ItemNotFoundException

    def get_item(self, pk: int) -> dict:
        if not self.dao.get_by_id(pk):
            raise self.not_found_exception
        return self.schema().dump(self.dao.get_by_id(pk))

    def get_all(self, page: int = 1, **kwargs) -> List[dict]:
        limit, offset = get_limit_and_offset(page)
        return self.schema(many=True).dump(self.dao.get_all(limit, offset))
