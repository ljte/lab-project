class BaseManagementException(Exception):
    pass


class NotFoundError(BaseManagementException):
    code = "not_found"


class DepartmentNotFoundError(NotFoundError):
    def __init__(self, department_id: str) -> None:
        self.message = f"Department {department_id} was not found"
        super().__init__(self.message)


class EmployeeNotFoundError(NotFoundError):
    def __init__(self, employee_id: str) -> None:
        self.message = f"Employee {employee_id} was not found"
        super().__init__(self.message)
