"""tests"""

from datetime import date

from department_app.models import db
from department_app.models.department import Department, Employee


def init_db_for_test():
    """populate db with test data"""
    deps = [Department(name='Finance department'),
            Department(name='Human Resource department'),
            Department(name='Accounting department'),
            Department(name='Sales department'),
            Department(name='Management department'),
            Department(name='Marketing department'),
            Department(name='Delete department'),
            Department(name='Edit department')]
    db.session.add_all(deps)
    db.session.commit()

    emps = [Employee(fullname='One Employee', salary=123, bday=date(1995, 12, 12), department_id=deps[0].id),
            Employee(fullname='Two Employee', salary=700, bday=date(1995, 12, 12), department_id=deps[2].id),
            Employee(fullname='Three Employee', salary=123, bday=date(1995, 12, 12), department_id=deps[1].id),
            Employee(fullname='Andrey Bobrov', salary=644, bday=date(1992, 6, 23), department_id=deps[3].id),
            Employee(fullname='Anna Volkova', salary=533, bday=date(1998, 10, 20), department_id=deps[4].id),
            Employee(fullname='Boris Nemchenko', salary=512, bday=date(1993, 6, 15), department_id=deps[5].id),
            Employee(fullname='Vladimir Novikov', salary=832, bday=date(1985, 9, 15), department_id=deps[5].id),
            Employee(fullname='Edit Employee', salary=1212, bday=date(1997, 12, 15), department_id=deps[4].id)]
    db.session.add_all(emps)
    db.session.commit()
