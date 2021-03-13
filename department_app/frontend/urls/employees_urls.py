from django.urls import path

from ..views import DeleteEmployeeView, EditEmployeeView, EmployeeView, PostEmployeeView

urlpatterns = [
    path(
        "employees/",
        EmployeeView.as_view(),
        name="employees",
    ),
    path(
        "delete_employee/<int:obj_id>",
        DeleteEmployeeView.as_view(),
        name="delete_employee",
    ),
    path(
        "edit_employee/<int:obj_id>",
        EditEmployeeView.as_view(),
        name="edit_employee",
    ),
    path(
        "add_employee/",
        PostEmployeeView.as_view(),
        name="add_employee",
    ),
]
