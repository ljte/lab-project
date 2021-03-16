from ..models import Employee
from ..serializers import EmployeeSchema
from ..service import get_all
from .resource import APIResource


class EmployeeView(APIResource):
    schema = EmployeeSchema
    model = Employee

    def get_queryset(self):
        query_dict = self.request.GET.dict()
        print(query_dict)
        pattern = query_dict.get("search_pattern", "")
        department_name = query_dict.get("department_name", "")
        bday = query_dict.get("bday", "")
        return get_all(
            self.model,
            fullname__icontains=pattern,
            department__name__contains=department_name,
            bday__contains=bday,
        )
