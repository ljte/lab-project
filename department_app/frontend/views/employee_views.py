import requests
from django.contrib import messages
from django.shortcuts import redirect

from .generics import (ConfigurableView, DeleteObjectView, EditObjectView,
                       ListObjectsView, PostObjectView)
from .helpers import errors_occurred

API_URL = "http://localhost:8000/api/employees/"


class BaseEmployeeView(ConfigurableView):
    api_url = API_URL

    def flash_message(self, request, obj, *, message=None, category=messages.SUCCESS):
        super().flash_message(
            request, obj["fullname"], message=message, category=category
        )

    def context_kwargs(self):
        resp = requests.get(API_URL.replace("employees", "departments"))
        if errors_occurred(self.request, resp):
            return redirect(self.redirect_view)
        return {"deps": resp.json()}


class EmployeeView(BaseEmployeeView, ListObjectsView):
    template_name = "employees/employees.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.context_kwargs())
        return context


class DeleteEmployeeView(DeleteObjectView, BaseEmployeeView):
    view_name = "employees"


class BaseEditEmployeeMixin(BaseEmployeeView):
    redirect_view = "employees"


class EditEmployeeView(EditObjectView, BaseEditEmployeeMixin):
    template_name = "employees/edit_employee.html"
    view_name = "edit_employee"


class PostEmployeeView(PostObjectView, BaseEditEmployeeMixin):
    template_name = "employees/add_employee.html"
    view_name = "add_employee"
