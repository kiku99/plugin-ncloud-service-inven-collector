from schematics import Model
from schematics.types import ModelType, ListType, StringType, IntType, DateTimeType, UnionType, MultiType, BooleanType, FloatType, DictType, \
    LongType
class HTTPHeaders(Model):
    date = StringType()
    x_clv_request_id = StringType(serialized_name='x-clv-request-id')
    x_clv_s3_version = StringType(serialized_name='x-clv-s3-version')
    accept_ranges = StringType(serialized_name='accept-ranges')
    x_amz_request_id = StringType(serialized_name='x-amz-request-id')
    content_type = StringType(serialized_name='content-type')
    content_length = StringType(serialized_name='content-length')

class Owner(Model):
    display_name = StringType()
    id = StringType()
class ResponseMetadata(Model):
    request_id = StringType()
    host_id = StringType()
    http_statuscode = IntType()
    http_headers = ModelType(HTTPHeaders)
    retry_attempts = IntType()
class Bucket(Model):
    name = StringType()
    creation_date = DateTimeType()

class BucketGroup(Model):
    ResponseMetadata = ModelType(ResponseMetadata)
    Buckets = ListType(ModelType(Bucket))
    Owner = ModelType(Owner)
