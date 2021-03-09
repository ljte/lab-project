from django.db.models import Q
from django.http.response import Http404
from django.shortcuts import get_object_or_404

from ..models import Employee
from ..serializers import EmployeeSchema as schema
from ..service import delete, save_obj, update
from .resource import APIResource


class EmployeeView(APIResource):
    def get(self, request, emp_id=None):
        if emp_id is None:
            pattern = request.GET.dict().get("search_pattern", "")
            emps = Employee.objects.filter(
                Q(first_name__contains=pattern) | Q(second_name__contains=pattern)
            ).all()
            emps = [schema.jsonify(e) for e in emps]
            return emps, 200
        try:
            emp = schema.jsonify(get_object_or_404(Employee, id=emp_id))
        except Http404:
            raise Http404(f"Employee with the id of {emp_id} was not found")
        return emp, 200

    def post(self, request):
        save_obj(schema.to_orm(request.POST.dict()))
        return "", 201

    def put(self, request, emp_id):
        updated_fields = schema.from_put(request.PUT)
        update(Employee, id=emp_id, **updated_fields)
        return "", 204

    def delete(self, request, emp_id):
        emp = delete(Employee, id=emp_id)
        return schema.jsonify(emp), 200
