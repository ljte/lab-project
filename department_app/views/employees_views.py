"""employees views"""

from datetime import datetime

from flask import (
    Blueprint, render_template, request, redirect, url_for, flash
)
from werkzeug.exceptions import BadRequestKeyError
import requests

employees_bp = Blueprint('employees', __name__,
                         template_folder='../templates')

API_URL = 'http://localhost:5000/api/employees'
DEP_API_URL = 'http://localhost:5000/api/departments'
fullname_filter = lambda emp: emp['fullname']


@employees_bp.route('/employees', methods=['GET'])
def index():
    """return all the employees
    """
    emps = requests.get(API_URL).json()['employees']
    deps = requests.get(DEP_API_URL).json()['departments']
    return render_template(
        'employees.html',
        employees=sorted(emps, key=fullname_filter),
        departments=deps,
        title='Employees'
    )


@employees_bp.route('/employees/add', methods=['GET', 'POST'])
def add():
    """add employee
    if user enters invalid data, flash an error
    """
    if request.method == 'POST':
        try:
            # if department was not chosen then the BadRequestKeyError is raised
            form = dict(request.form)
            emp = {
                'fullname': form['fullname'],
                'bday': form['bday'],
                'salary': form['salary'],
                'dep_name': form['dep_name']
            }
        except (BadRequestKeyError, KeyError):
            flash("Choose a department", category='danger')
            return redirect(url_for('employees.add'))
        response = requests.post(API_URL, data=emp)
        if response.status_code != 201:
            flash(response.json()['message'], category='danger')
            return redirect(url_for('employees.add'))

        flash(f"Successfully added {emp['fullname']}", category='success')
        return redirect((url_for('employees.index')))

    deps = requests.get(DEP_API_URL).json()['departments']
    return render_template('add_employee.html', title='New Employee', departments=deps)


@employees_bp.route('/employees/delete/<int:employee_id>', methods=['GET'])
def delete(employee_id: int):
    """delete the employee with id=employee_id

    employee_id: the id of the requested employee
    """
    emp = requests.get(API_URL + f'/{employee_id}').json()
    response = requests.delete(API_URL + f'/{employee_id}')
    if response.status_code != 204:
        flash(response.json()['message'], category='danger')
    else:
        flash(f"Succesfully deleted {emp['fullname']}", category='success')
    return redirect(url_for('employees.index'))


@employees_bp.route('/employees/edit/<int:employee_id>', methods=['GET', 'POST'])
def edit(employee_id: int):
    """update the emploeey's fields

    employee_id: id of the requested employee
    """
    emp = requests.get(API_URL + f'/{employee_id}')
    if emp.status_code != 200:
        flash(emp.json()['message'], category='danger')
        return redirect(url_for('employees.index'))
    emp = emp.json()
    if request.method == 'POST':
        form = dict(request.form)
        response = requests.put(API_URL + f'/{employee_id}', data=form)
        if response.status_code != 204:
            flash(response.json()['message'], category='danger')
            return redirect(url_for('employees.edit', employee_id=employee_id))

        flash(f"Successfully updated {form['fullname']}", category='success')
        return redirect(url_for('employees.index'))

    emp['bday'] = datetime.strptime(emp['bday'], '%d-%m-%Y')
    deps = requests.get(DEP_API_URL).json()['departments']
    return render_template('edit_employee.html', title='Edit employee', emp=emp, departments=deps)


@employees_bp.route('/employees/search', methods=['GET', 'POST'])
def search():
    """return only the employee specified by 'search_string'
    """
    search_string = request.form.get('search_string', '')
    emps = requests.get(API_URL, data={'search_string': search_string}).json()['employees']
    deps = requests.get(DEP_API_URL).json()['departments']
    return render_template(
        'employees.html',
        employees=sorted(emps, key=fullname_filter),
        departments=deps,
        title='Employees'
    )


@employees_bp.route('/employees/filter_by_department', methods=['GET', 'POST'])
def filter_by_department():
    """return the employee with the specified department
    """
    if request.method == 'POST':
        dep_name = request.form.get('department', '')
        if dep_name == '':
            flash("Choose a department's name", category='info')
            return redirect(url_for('employees.index'))

        emps = [emp for emp in requests.get(API_URL).json()['employees']
                if emp['department'] == dep_name]

        deps = requests.get(DEP_API_URL).json()['departments']
        return render_template(
            'employees.html',
            employees=sorted(emps, key=fullname_filter),
            departments=deps,
            title='Employees'
        )

    return redirect(url_for('employees.index'))


@employees_bp.route('/employees/filter_by_bday', methods=['GET', 'POST'])
def filter_by_bday():
    """return the employee who were born on a specific bady or
    in a specific period
    """
    if request.method == 'POST':
        deps = requests.get(DEP_API_URL).json()['departments']
        form = dict(request.form)
        bday = form.get('bday', '')
        if bday != '':
            response = requests.get(API_URL + '/filter_by_bday', data={'bday': bday})
            if response.status_code != 200:
                flash(response.json()['message'], category='danger')
                return redirect(url_for('employees.index'))
            emps = response.json()['employees']
            return render_template(
                'employees.html',
                employees=sorted(emps, key=fullname_filter),
                departments=deps,
                title='Employees'
            )

        start_date = form.get('start_date', '')
        end_date = form.get('end_date', '')
        if start_date != '' and end_date != '':
            response = requests.get(API_URL + '/filter_by_date_period',
                                    data={
                                        'start_date': start_date,
                                        'end_date': end_date
                                    })
            if response.status_code != 200:
                flash(response.json()['message'], category='danger')
                return redirect(url_for('employees.index'))
            emps = response.json()['employees']
            return render_template(
                'employees.html',
                employees=emps,
                departments=deps,
                title='Employees'
            )
    flash('You must specify both start and end dates or choose a birthday', category='info')
    return redirect(url_for('employees.index'))
