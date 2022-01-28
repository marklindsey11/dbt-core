from dbt.lazy import Lazy
from mashumaro import DataClassDictMixin
from mashumaro.config import (
    BaseConfig as MashBaseConfig
)
from mashumaro.types import SerializationStrategy
from typing import Dict, List


# The dbtClassMixin serialization class has a DateTime serialization strategy
# class. If a datetime ends up in an event class, we could use a similar class
# here to serialize it in our preferred format.

class ExceptionSerialization(SerializationStrategy):
    def serialize(self, value):
        out = str(value)
        return out

    def deserialize(self, value):
        return (Exception(value))


class BaseExceptionSerialization(SerializationStrategy):
    def serialize(self, value):
        return str(value)

    def deserialize(self, value):
        return (BaseException(value))


# this is not really generic. These functions must know about every concrete usage
# of the generic type and serialize all wrapped types. There is lots of room for
# runtime errors because we have to match up the types by hand here, and make sure
# we didn't miss any.
class LazySerialization1(SerializationStrategy):
    def serialize(self, value):
        return str(value.force())

    def deserialize(self, value):
        raise Exception("can't deserialize a generic Lazy value")


# This class is the equivalent of dbtClassMixin that's used for serialization
# in other parts of the code. That class did extra things which we didn't want
# to use for events, so this class is a simpler version of dbtClassMixin.
class EventSerialization(DataClassDictMixin):

    class Config(MashBaseConfig):
        serialization_strategy = {
            Exception: ExceptionSerialization(),
            BaseException: ExceptionSerialization(),
            Lazy[Dict[str, List[str]]]: LazySerialization1()
        }
