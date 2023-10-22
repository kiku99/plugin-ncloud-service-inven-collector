from schematics import Model
from schematics.types import ModelType, ListType, StringType, IntType, DateTimeType, UnionType, MultiType, BooleanType, FloatType, DictType, \
    LongType


class ArchiveBucketGroup(Model):
    name = StringType()
    count = IntType()
    bytes = IntType()
    last_modified = DateTimeType()
