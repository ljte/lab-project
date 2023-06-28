import abc

from management.domain.model import Department, Employee


class IDepartmentRepository(abc.ABC):
    @abc.abstractmethod
    def save(self, department: Department) -> None:
        pass

    @abc.abstractmethod
    def find(self, department_id: str) -> None:
        pass

    @abc.abstractmethod
    def delete(self, department_id: str) -> None:
        pass


class IEmployeeRepository(abc.ABC):
    @abc.abstractmethod
    def save(self, employee: Employee) -> None:
        pass

    @abc.abstractmethod
    def find(self, employee_id: str) -> None:
        pass

    @abc.abstractmethod
    def all_employees_of_department(self, department_id: str) -> list[Employee]:
        pass

    @abc.abstractmethod
    def delete(self, employee_id: str) -> None:
        pass
