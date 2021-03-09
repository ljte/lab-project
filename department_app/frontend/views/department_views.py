import requests
from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.generic import View

API_URL = "http://localhost:8000/api"


class DepartmentView(View):
    http_method_names = ["get"]

    def get(self, request):
        pattern = request.GET.dict().get("search_pattern", "")
        resp = requests.get(f"{API_URL}/departments/", f"search_pattern={pattern}")
        if resp.status_code != 200:
            messages.info(request, resp.json().get("message"))
            return render(request, "departments/departments.html")
        context = {"deps": resp.json()}
        return render(request, "departments/departments.html", context)


class DeleteDepartmentView(View):
    http_method_names = ["get"]

    def get(self, request, dep_id):
        resp = requests.delete(f"{API_URL}/departments/{dep_id}")
        if resp.status_code != 200:
            messages.error(request, resp.json().get("message"))
            return redirect("departments")
        dep = resp.json()
        messages.success(request, f"Successfully deleted {dep['name']}")
        return redirect("departments")


class EditDepartmentView(View):
    http_method_names = ["get", "post"]

    def get(self, request, dep_id):
        resp = requests.get(f"{API_URL}/departments/{dep_id}")
        if resp.status_code != 200:
            messages.error(request, resp.json().get("message"))
            return redirect("departments")
        dep = resp.json()
        return render(request, "departments/edit_department.html", {"dep": dep})

    def post(self, request, dep_id):
        resp = requests.get(f"{API_URL}/departments/{dep_id}")
        if resp.status_code != 200:
            messages.error(request, resp.json().get("message"))
            return redirect("departments")
        dep = resp.json()
        put = request.POST.dict()
        if dep["name"] != put["name"]:
            resp = requests.put(
                f"{API_URL}/departments/{dep_id}",
                data=put,
            )
            if resp.status_code != 204:
                messages.error(request, resp.json().get("message"))
                return redirect("edit_department", dep_id=dep_id)
            messages.info(
                request, f"Successfully changed {dep['name']} to {put['name']}"
            )
        return redirect("departments")


class PostDepartmentView(View):
    http_method_names = ["get", "post"]

    def get(self, request):
        return render(request, "departments/add_department.html")

    def post(self, request):
        data = request.POST.dict()
        resp = requests.post(f"{API_URL}/departments/", data=data)
        if resp.status_code != 201:
            messages.error(request, resp.json().get("message"))
            return redirect("add_department")
        messages.success(request, f"Successfully added {data['name']}")
        return redirect("departments")
