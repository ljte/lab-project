from ..models import Employee
from ..serializers import EmployeeSchema
from ..service import get_all
from .resource import APIResource


class EmployeeView(APIResource):
    schema = EmployeeSchema
    model = Employee
    http_method_names = ["get", "post", "put", "delete"]

    def get_queryset(self):
        query_dict = self.request.GET.dict()
        pattern = query_dict.get("search_pattern", "")
        department_name = query_dict.get("department_name", "")
        start_date = query_dict.get("start_date", "")
        end_date = query_dict.get("end_date", "")
        if start_date and end_date:
            return get_all(
                self.model,
                department__name__contains=department_name,
                bday__range=[start_date, end_date],
            )
        return get_all(
            self.model,
            fullname__icontains=pattern,
            department__name__contains=department_name,
        )
