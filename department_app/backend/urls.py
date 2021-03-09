from django.urls import path

from .views import DepartmentView, EmployeeView

urlpatterns = [
    path("departments/", DepartmentView.as_view()),
    path("departments/<int:dep_id>", DepartmentView.as_view()),
    path("employees/", EmployeeView.as_view()),
    path("employees/<int:emp_id>", EmployeeView.as_view()),
]
