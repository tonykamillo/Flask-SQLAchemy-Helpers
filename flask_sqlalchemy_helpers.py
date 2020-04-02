import uuid
from datetime import datetime

import sqlalchemy.types as types
from sqlalchemy import Column, ForeignKey, String, DateTime, Integer
from sqlalchemy.ext.declarative import declared_attr

from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy, BaseQuery, Model as SAModel


def m2m(db, table1, table2):
    if not isinstance(table1, str):
        table1 = table1.__name__

    if not isinstance(table2, str):
        table2 = table2.__name__

    table1 = table1.lower()
    field1 = '%s_id' % table1
    f_key1 = '%s.id' % table1

    table2 = table2.lower()
    field2 = '%s_id' % table2
    f_key2 = '%s.id' % table2

    table_name = '%s_%s_m2m' % (table1, table2)

    return db.Table(
        table_name,
        db.Column(field1, UUID, db.ForeignKey(f_key1)),
        db.Column(field2, UUID, db.ForeignKey(f_key2))
    )


class UUID(types.TypeDecorator):

    impl = types.String

    def process_bind_param(self, value, dialect):
        if value:
            value = str(value)
        return value

    def process_result_value(self, value, dialect):
        if value and not isinstance(value, uuid.UUID):
            value = uuid.UUID(value)
        return value


class JoinedInheritanceMixin:

    @declared_attr
    def _model_type(cls):
        return Column(String(50))

    @declared_attr
    def __mapper_args__(cls):

        indentity = cls.__name__.lower()
        mapper_args = {'polymorphic_identity': indentity}

        if JoinedInheritanceMixin in cls.__bases__:
            mapper_args.update({'polymorphic_on': cls._model_type})

        return mapper_args


class ModelUUID(SAModel):

    @declared_attr.cascading
    def id(cls):
        args = [UUID]
        kwargs = dict(primary_key=True)

        if JoinedInheritanceMixin in cls.mro() and JoinedInheritanceMixin not in cls.__bases__:
            args.append(ForeignKey('%s.id' % cls.__bases__[0].__name__.lower()))
        else:
            kwargs.update(default=uuid.uuid4)
        return Column(*args, **kwargs)


class Query(BaseQuery):

    @property
    def non_deleted(self):
        return self.filter_by(deleted=False)


class SQLAlchemyDRY(_SQLAlchemy):

    def __init__(self, *args, **kwargs):
        kwargs.update(model_class=ModelUUID, query_class=Query)

        super(SQLAlchemyDRY, self).__init__(*args, **kwargs)

        self.UUID = UUID

    def m2m(self, t1, t2):
        return m2m(self, t1, t2)
