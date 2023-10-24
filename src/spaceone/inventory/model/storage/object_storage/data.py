from schematics import Model
from schematics.types import ModelType, ListType, StringType, IntType, DateTimeType, UnionType, MultiType, BooleanType, FloatType, DictType, \
    LongType


class Owner(Model):
    display_name = StringType()
    id = StringType()

class Buckets(Model):
    name = StringType()
    creation_date = DateTimeType()

class BucketGroup(Model):
    buckets = ModelType(Buckets)
    owner = ModelType(Owner)

