from django.contrib import messages

from .generics import (DeleteObjectView, EditObjectView, ListObjectsView,
                       PostObjectView)

API_URL = "http://localhost:8000/api/departments/"


class DepartmentView(ListObjectsView):
    template_name = "departments/departments.html"
    context_object_name = "departments"
    api_url = API_URL


class DeleteDepartmentView(DeleteObjectView):
    view_name = "departments"
    api_url = API_URL

    def flash_message(self, request, obj, *, message=None, category=messages.SUCCESS):
        super().flash_message(request, obj["name"], message=message, category=category)


class EditDepartmentView(EditObjectView):
    template_name = "departments/edit_department.html"
    view_name = "edit_department"
    redirect_view = "departments"
    api_url = API_URL

    def flash_message(self, request, obj, *, message=None, category=messages.SUCCESS):
        super().flash_message(request, obj["name"], message=message, category=category)


class PostDepartmentView(PostObjectView):
    template_name = "departments/add_department.html"
    view_name = "add_department"
    api_url = API_URL
    redirect_view = "departments"

    def flash_message(self, request, obj, *, message=None, category=messages.SUCCESS):
        super().flash_message(request, obj["name"], message=message, category=category)
