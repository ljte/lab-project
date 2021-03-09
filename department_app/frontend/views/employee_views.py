import requests
from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.generic import View

API_URL = "http://localhost:8000/api"


class EmployeeView(View):
    http_method_names = ["get"]

    def get(self, request):
        pattern = request.GET.dict().get("search_pattern", "")
        resp = requests.get(f"{API_URL}/employees/", f"search_pattern={pattern}")
        if resp.status_code != 200:
            messages.info(request, resp.json().get("message"))
            return render(request, "employees/employees.html")
        context = {"emps": resp.json()}
        return render(request, "employees/employees.html", context)


class DeleteEmployeeView(View):
    http_method_names = ["get"]

    def get(self, request, emp_id):
        resp = requests.delete(f"{API_URL}/employees/{emp_id}")
        if resp.status_code != 200:
            messages.error(request, resp.json().get("message"))
            return redirect("employees")
        emp = resp.json()
        messages.success(
            request, f"Successfully deleted {emp['first_name']} {emp['second_name']}"
        )
        return redirect("employees")


class EditEmployeeView(View):
    http_method_names = ["get", "post"]

    def get(self, request, emp_id):
        resp = requests.get(f"{API_URL}/employees/{emp_id}")
        if resp.status_code != 200:
            messages.error(request, resp.json().get("message"))
            return redirect("employees")
        emp = resp.json()
        deps = requests.get(f"{API_URL}/departments/").json()
        return render(
            request, "employees/edit_employee.html", {"emp": emp, "deps": deps}
        )

    def post(self, request, emp_id):
        resp = requests.get(f"{API_URL}/employees/{emp_id}")
        if resp.status_code != 200:
            messages.error(request, resp.json().get("message"))
            return redirect("employees")
        emp = resp.json()
        put = self.parse_put_dict(emp, request.POST.dict())
        if put != {}:
            resp = requests.put(
                f"{API_URL}/employees/{emp_id}",
                data=put,
            )
            if resp.status_code != 204:
                messages.error(request, resp.json().get("message"))
                return redirect("edit_employee", emp_id=emp_id)
            messages.info(
                request,
                f"Successfully changed {emp['first_name']} {emp['second_name']}",
            )
        return redirect("employees")

    def parse_put_dict(self, emp, put):
        return {
            key: put[key]
            for key, val in emp.items()
            if key != "id" and str(val) != str(put[key])
        }


class PostEmployeeView(View):
    http_method_names = ["get", "post"]

    def get(self, request):
        deps = requests.get(f"{API_URL}/departments/").json()
        return render(request, "employees/add_employee.html", {"deps": deps})

    def post(self, request):
        data = request.POST.dict()
        resp = requests.post(f"{API_URL}/employees/", data=data)
        if resp.status_code != 201:
            messages.error(request, resp.json().get("message"))
            return redirect("add_employee")
        messages.info(
            request, f"Successfully added {data['first_name']} {data['second_name']}"
        )
        return redirect("employees")
