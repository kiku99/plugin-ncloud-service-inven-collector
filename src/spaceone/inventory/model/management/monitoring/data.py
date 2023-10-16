from schematics import Model
from schematics.types import ModelType, ListType, StringType, IntType, DateTimeType, BooleanType, FloatType, DictType, \
    LongType


class Metric(Model):
    instance_no = StringType()
    metric_name = StringType()

class DataPoint(Model):
        timestamp = StringType()
        average = FloatType()
        unit = StringType()

class MetricData(Model):
    label = StringType()
    average = FloatType()
    maximum = FloatType()
    minimum = FloatType()
    sum = FloatType()
    data_point_list = ListType(ModelType(DataPoint))



class MetricStatistic(Model):
    instance_no = StringType()
    metric_data_list = ListType(ModelType(MetricData))



