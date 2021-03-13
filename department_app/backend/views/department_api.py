from ..models import Department
from ..serializers import DepartmentSchema
from ..service import get_all
from .resource import APIResource


class DepartmentView(APIResource):
    schema = DepartmentSchema
    model = Department

    def get_queryset(self):
        pattern = self.request.GET.dict().get("search_pattern", "")
        return get_all(self.model, name__icontains=pattern)
