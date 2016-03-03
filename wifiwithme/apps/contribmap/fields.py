import collections

from django.db import models


class CommaSeparatedList(list):
    """ str representation is useful for displayint in forms
    """
    def __str__(self):
        return ','.join(self)


class CommaSeparatedCharField(models.CharField):
    "Implements comma-separated storage of lists"

    def from_db_value(self, value, expression, connection, context):
        if value is None:
            return value
        return CommaSeparatedList(value.split(','))

    def to_python(self, value):
        if isinstance(value, CommaSeparatedList):
            return value

        if value is None:
            return value

        return CommaSeparatedList([i.strip() for i in value.split(',')])

    def get_prep_value(self, value):
        if isinstance(value, collections.Iterable):
            return ','.join(value)
        else:
            return value
