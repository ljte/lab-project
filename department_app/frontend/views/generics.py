"""classes in this module are not supposed to be used directly"""

from urllib.parse import urlencode

import requests
from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.generic import ListView, View

from .helpers import errors_occurred


class ConfigurableView(View):
    api_url = None
    view_name = None
    message = None
    redirect_view = None
    template_name = None

    def flash_message(self, request, obj, *, message=None, category=messages.SUCCESS):
        messages.add_message(request, category, (self.message % obj) or message)

    def get_api_url(self, obj_id):
        url = "%s/%d" % (self.api_url.rstrip("/"), obj_id)
        return url

    def get_context(self, **kwargs):
        context = kwargs
        if hasattr(self, "context_kwargs"):
            context.update(self.context_kwargs)
        return context


class ListObjectsView(ListView):
    http_method_names = ["get"]
    api_url = None

    def get_queryset(self):
        query = urlencode(self.request.GET.dict())
        resp = requests.get(self.api_url, query)
        if errors_occurred(self.request, resp):
            return []
        return resp.json()


class DeleteObjectView(ConfigurableView):
    http_method_names = ["get", "delete"]
    message = "Successfully deleted %s"

    def delete(self, request, obj_id):
        resp = requests.delete(self.get_api_url(obj_id))
        if errors_occurred(request, resp):
            return redirect(self.view_name)
        obj = resp.json()
        self.flash_message(request, obj)
        return redirect(self.view_name)

    def get(self, request, obj_id):
        return self.delete(request, obj_id)


class EditObjectView(ConfigurableView):
    http_method_names = ["get", "post", "put"]
    message = "Successfully edited %s"

    def get_object(self, obj_id):
        resp = requests.get(self.get_api_url(obj_id))
        if errors_occurred(self.request, resp):
            return None
        return resp.json()

    def get(self, request, obj_id):
        obj = self.get_object(obj_id)
        if obj is None:
            return redirect(self.redirect_view)
        return render(request, self.template_name, self.get_context(object=obj))

    def put(self, request, obj_id):
        obj = self.get_object(obj_id)
        if obj is None:
            return redirect(self.redirect_view)
        put_data = self._parse_put_dict(obj, request.POST.dict())
        if put_data != {}:
            resp = requests.put(self.get_api_url(obj_id), data=put_data)
            if errors_occurred(request, resp):
                return redirect(self.view_name, obj_id=obj_id)
            self.flash_message(request, obj)
        return redirect(self.redirect_view)

    def post(self, request, obj_id):
        return self.put(request, obj_id)

    @staticmethod
    def _parse_put_dict(obj, put_dict):
        keys = obj.keys() & put_dict.keys()
        return {
            key: put_dict[key] for key in keys if str(obj[key]) != str(put_dict[key])
        }


class PostObjectView(ConfigurableView):
    http_method_names = ["get", "post"]
    message = "Successfully added %s"

    def get(self, request):
        return render(request, self.template_name, self.get_context())

    def post(self, request):
        obj = request.POST.dict()
        resp = requests.post(self.api_url, data=obj)
        if errors_occurred(request, resp):
            return redirect(self.view_name)
        self.flash_message(request, obj)
        return redirect(self.redirect_view)
