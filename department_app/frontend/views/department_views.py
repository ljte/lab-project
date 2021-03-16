from django.contrib import messages

from .generics import (ConfigurableView, DeleteObjectView, EditObjectView,
                       ListObjectsView, PostObjectView)

API_URL = "http://localhost:8000/api/departments/"


class BaseDepartmentView(ConfigurableView):
    api_url = API_URL
    redirect_view = "departments"

    def flash_message(self, request, obj, *, message=None, category=messages.SUCCESS):
        super().flash_message(request, obj["name"], message=message, category=category)


class DepartmentView(BaseDepartmentView, ListObjectsView):
    template_name = "departments/departments.html"
    context_object_name = "departments"


class DeleteDepartmentView(BaseDepartmentView, DeleteObjectView):
    view_name = "departments"


class EditDepartmentView(BaseDepartmentView, EditObjectView):
    template_name = "departments/edit_department.html"
    view_name = "edit_department"


class PostDepartmentView(BaseDepartmentView, PostObjectView):
    template_name = "departments/add_department.html"
    view_name = "add_department"
