from django.urls import path

from .views import DepartmentView, EmployeeView, HealthcheckView

urlpatterns = [
    path("departments/", DepartmentView.as_view()),
    path("departments/<int:obj_id>", DepartmentView.as_view()),
    path("employees/", EmployeeView.as_view()),
    path("employees/<int:obj_id>", EmployeeView.as_view()),
    path("healthcheck/", HealthcheckView.as_view()),
]
