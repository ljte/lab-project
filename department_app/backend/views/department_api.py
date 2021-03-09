from django.http.response import Http404
from django.shortcuts import get_object_or_404

from ..models import Department
from ..serializers import DepartmentSchema as schema
from ..service import delete, save_obj, update
from .resource import APIResource


class DepartmentView(APIResource):
    def get(self, request, dep_id=None):
        if dep_id is None:
            pattern = request.GET.dict().get("search_pattern", "")
            deps = [
                schema.jsonify(d)
                for d in Department.objects.filter(name__contains=pattern).all()
            ]
            return deps, 200
        try:
            dep = schema.jsonify(get_object_or_404(Department, id=dep_id))
        except Http404:
            raise Http404(f"Department with the id of {dep_id} does not exist")
        return dep, 200

    def post(self, request):
        save_obj(schema.to_orm(request.POST.dict()))
        return "", 201

    def put(self, request, dep_id):
        updated = schema.parse_obj(request.PUT)
        update(Department, id=dep_id, **updated)
        return "", 204

    def delete(self, request, dep_id):
        dep = delete(Department, id=dep_id)
        return schema.jsonify(dep), 200
