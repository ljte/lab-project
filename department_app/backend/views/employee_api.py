from ..models import Employee
from ..serializers import EmployeeSchema
from ..service import get_all
from .resource import APIResource


class EmployeeView(APIResource):
    schema = EmployeeSchema
    model = Employee

    def get_queryset(self):
        pattern = self.request.GET.dict().get("search_pattern", "")
        return get_all(self.model, fullname__icontains=pattern)
