"""department views"""

import os

from flask import (
    Blueprint, render_template, redirect, url_for, request, flash
)
import requests

from department_app.service import utils


department_bp = Blueprint('departments', __name__,
                          template_folder='../templates')
API_URL = f"{os.environ.get('URL')}/api/departments"


@department_bp.route('/', methods=['GET'])
@department_bp.route('/departments/', methods=['GET'])
def index():
    """when the user enters this route
    show him the list of all the department
    """
    deps = requests.get(API_URL).json()['departments']
    return render_template(
        'departments.html',
        departments=sorted(deps, key=lambda dep: dep['name']),
        title='Departments'
    )


@department_bp.route('/departments/add', methods=['GET', 'POST'])
def add():
    """if method is GET then just show the form for a new department
    if method is POST then try to add the new department or
    flash an error message
    """
    if request.method == 'POST':
        dep = {'name': request.form['name']}
        response = requests.post(API_URL, data=dep)
        if response.status_code != 201:
            flash(response.json()['message'], category='danger')
            return redirect(url_for('departments.add'))

        flash(f"Successfully added {dep['name']}", category='success')
        return redirect((url_for('departments.index')))

    return render_template('add_department.html', title='New department')


@department_bp.route('/departments/delete/<int:department_id>', methods=['GET'])
def delete(department_id: int):
    """delete the requested department
    a department can be deleted only if
    it has no employees.

    department_id: id of the requested department
    """
    dep = requests.get(API_URL + f'/{department_id}').json()
    response = requests.delete(API_URL + f'/{department_id}')
    if response.status_code != 204:
        flash(response.json()['message'], category='danger')
    else:
        flash(f"Successfully deleted {dep['name']}", category='success')
    return redirect(url_for('departments.index'))


@department_bp.route('/departments/edit/<int:department_id>', methods=['GET', 'POST'])
def edit(department_id: int):
    """update the department's name

    department_id: id of the requested department
    """
    dep = requests.get(API_URL + f'/{department_id}')
    if dep.status_code != 200:
        flash(dep.json()['message'], category='danger')
        return redirect(url_for('departments.index'))
    dep = dep.json()

    if request.method == 'POST':
        data = {'name': request.form['name']}
        response = requests.put(API_URL + f'/{department_id}', data=data)
        if response.status_code != 204:
            flash(response.json()['message'], category='danger')
            return redirect(url_for('departments.edit', department_id=department_id))

        flash(f"Successfully changed {dep['name']} to {data['name']}", category='success')
        return redirect(url_for('departments.index'))

    return render_template('edit_department.html', title='Edit department', dep=dep)


@department_bp.route('/departments/search', methods=['GET', 'POST'])
def search():
    """return the department which names resemble to 'search_string'
    """
    search_string = request.form.get('search_string', '')
    deps = requests.get(API_URL, data={'search_string': search_string}).json()['departments']
    return render_template('departments.html', departments=deps, title='Departments')


@department_bp.route('/departments/filter_by_salary', methods=['GET', 'POST'])
def filter_by_salary():
    """filter department down by the given average salary
    """
    if request.method == 'POST':
        form = dict(request.form)
        average_salary = form['average_salary']

        if average_salary == '' or not average_salary.isnumeric():
            flash('Invalid average salary', category='info')
            return redirect(url_for('departments.index'))

        average_salary = float(average_salary)
        operator = form.get('comparison', '>')
        try:
            deps = [dep for dep in requests.get(API_URL).json()['departments']
                    if utils.compare(dep['average_salary'], average_salary, operator)]
        except ValueError as exc:
            flash(str(exc), category='info')
            return redirect(url_for('departments.index'))

        return render_template('departments.html', departments=deps, title='Departments')

    return redirect(url_for('departments.index'))
