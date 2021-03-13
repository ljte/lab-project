from django.db.models import Model
from pydantic import BaseModel


class ORMModel(BaseModel):
    class Config:
        orm_mode = True

    @classmethod
    def dump_obj(cls, obj):
        raise NotImplementedError

    @classmethod
    def dumps(cls, obj):
        # check if obj is a list or a single object and return their dicts
        if isinstance(obj, list):
            return [cls.dump_obj(d) for d in obj]
        elif isinstance(obj, Model):
            return cls.dump_obj(obj)
        else:
            ValueError("Invalid object %s" % obj)

    @classmethod
    def loads(cls, obj_dict, model):
        # validate and parse dep_dict and return an instance of Department class
        d = cls.parse_obj(obj_dict)
        return model.from_dict(d.dict())

    @classmethod
    def process(cls, obj_dict):
        # validate, parse and return dict, not a schema object
        obj = cls.parse_obj(obj_dict)
        return obj.dict()
