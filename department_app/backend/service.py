from django.db import IntegrityError
from django.http import Http404
from django.shortcuts import get_object_or_404


def save_obj(obj):
    try:
        obj.save()
    except IntegrityError as e:
        raise ValueError(f"{obj} already exists") from e
    except AttributeError as e:
        raise ValueError(
            f"Invalid {obj} is of type {type(obj)}, must be a model"
        ) from e


def update(model, id, **new_fields):
    try:
        query_set = model.objects.filter(id=id)
    except AttributeError as e:
        raise ValueError(
            f"Invalid {model} is of type {type(model)}, must be a model"
        ) from e
    if not query_set.exists():
        raise Http404(f"{model.__name__} with id of `{id} does not exist")
    query_set.update(**new_fields)


def delete(model, id):
    try:
        obj = get_object_or_404(model, id=id)
    except ValueError as e:
        raise ValueError(
            f"Invalid {model} is of type {type(model)}, must be a model"
        ) from e
    except Http404:
        raise Http404(f"{model.__name__} with the id of {id} does not exist")
    obj.delete()
    return obj
