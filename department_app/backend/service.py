from django.db import IntegrityError
from django.http import Http404
from django.shortcuts import get_list_or_404, get_object_or_404


def get_all(model, **filter_kwargs):
    try:
        return get_list_or_404(model, **filter_kwargs)
    except Http404:
        return []


def get_obj(model, **filter_kwargs):
    try:
        return get_object_or_404(model, **filter_kwargs)
    except Http404:
        raise Http404(f"{model.__name__} with `{filter_kwargs}` does not exist")


def save_obj(obj):
    try:
        obj.save()
    except IntegrityError as e:
        raise ValueError(f"{obj} already exists") from e
    except AttributeError as e:
        raise ValueError(
            f"Invalid {obj} is of type {type(obj)}, must be a model"
        ) from e


def update(model, id, new_fields):
    try:
        obj = get_obj(model, id=id)
        for key, val in new_fields.items():
            if val is not None:
                setattr(obj, key, val)
        obj.save()
    except AttributeError as e:
        raise ValueError(
            f"Invalid {model} is of type {type(model)}, must be a model"
        ) from e


def delete(model, id):
    try:
        obj = get_obj(model, pk=id)
    except ValueError as e:
        raise ValueError(
            f"Invalid {model} is of type {type(model)}, must be a model"
        ) from e
    obj.delete()
    return obj
