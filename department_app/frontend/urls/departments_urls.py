from django.urls import path

from ..views import (
    DeleteDepartmentView,
    DepartmentView,
    EditDepartmentView,
    PostDepartmentView,
)

urlpatterns = [
    path("", DepartmentView.as_view(), name="index"),
    path("departments/", DepartmentView.as_view(), name="departments"),
    path(
        "delete_department/<int:dep_id>",
        DeleteDepartmentView.as_view(),
        name="delete_department",
    ),
    path(
        "edit_department/<int:dep_id>",
        EditDepartmentView.as_view(),
        name="edit_department",
    ),
    path(
        "add_department/",
        PostDepartmentView.as_view(),
        name="add_department",
    ),
]
