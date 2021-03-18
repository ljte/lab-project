import operator

from ..models import Department
from ..serializers import DepartmentSchema
from ..service import get_all
from .resource import APIResource


class DepartmentView(APIResource):
    http_method_names = ["get", "post", "put", "delete"]
    schema = DepartmentSchema
    model = Department
    operations = {
        "=": operator.eq,
        "<>": operator.ne,
        ">=": operator.ge,
        "<=": operator.le,
        ">": operator.gt,
        "<": operator.lt,
    }

    def filter_by_salary(self, salary, comparison_operator):
        operation = self.operations[comparison_operator]

        def compare(department):
            return operation(department.average_salary, salary)

        return compare

    def get_queryset(self):
        query_dict = self.request.GET.dict()
        pattern = query_dict.get("search_pattern", "")
        comparison_operator = query_dict.get("comparison_operator", "")
        if comparison_operator:
            try:
                salary = float(query_dict.get("salary", ""))
                filter_func = self.filter_by_salary(salary, comparison_operator)
                deps = filter(filter_func, get_all(self.model))
                return list(deps)
            except ValueError:
                raise ValueError("Salary is empty")
            except KeyError:
                raise ValueError(
                    "Invalid comparison operator `%s`" % comparison_operator
                )
        return get_all(self.model, name__icontains=pattern)
