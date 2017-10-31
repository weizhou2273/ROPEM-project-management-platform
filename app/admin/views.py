# app/admin/views.py

from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from . import admin
from forms import DepartmentForm,EmployeeAssignForm, RoleForm,ProjectAssignForm
from .. import db
from ..models import Department,Role,Employee,Project

def check_admin():
    """
    Prevent non-admins from accessing the page
    """
    if not current_user.is_admin:
        abort(403)

# Department Views

@admin.route('/departments', methods=['GET', 'POST'])
@login_required
def list_departments():
    """
    List all departments
    """
    check_admin()

    departments = Department.query.all()

    return render_template('admin/departments/departments.html',
                           departments=departments, title="Departments")

@admin.route('/departments/add', methods=['GET', 'POST'])
@login_required
def add_department():
    """
    Add a department to the database
    """
    check_admin()

    add_department = True

    form = DepartmentForm()
    if form.validate_on_submit():
        department = Department(name=form.name.data,
                                description=form.description.data)
        try:
            # add department to the database
            db.session.add(department)
            db.session.commit()
            flash('You have successfully added a new department.')
        except:
            # in case department name already exists
            flash('Error: department name already exists.')

        # redirect to departments page
        return redirect(url_for('admin.list_departments'))

    # load department template
    return render_template('admin/departments/department.html', action="Add",
                           add_department=add_department, form=form,
                           title="Add Department")

@admin.route('/departments/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_department(id):
    """
    Edit a department
    """
    check_admin()

    add_department = False

    department = Department.query.get_or_404(id)
    form = DepartmentForm(obj=department)
    if form.validate_on_submit():
        department.name = form.name.data
        department.description = form.description.data
        db.session.commit()
        flash('You have successfully edited the department.')

        # redirect to the departments page
        return redirect(url_for('admin.list_departments'))

    form.description.data = department.description
    form.name.data = department.name
    return render_template('admin/departments/department.html', action="Edit",
                           add_department=add_department, form=form,
                           department=department, title="Edit Department")

@admin.route('/departments/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_department(id):
    """
    Delete a department from the database
    """
    check_admin()

    department = Department.query.get_or_404(id)
    db.session.delete(department)
    db.session.commit()
    flash('You have successfully deleted the department.')

    # redirect to the departments page
    return redirect(url_for('admin.list_departments'))

    return render_template(title="Delete Department")


# Role Views
@admin.route('/roles')
@login_required
def list_roles():
    check_admin()
    """
    List all roles
    """
    roles = Role.query.all()
    return render_template('admin/roles/roles.html',
                           roles=roles, title='Roles')

@admin.route('/roles/add', methods=['GET', 'POST'])
@login_required
def add_role():
    """
    Add a role to the database
    """
    check_admin()

    add_role = True

    form = RoleForm()
    if form.validate_on_submit():
        role = Role(name=form.name.data,
                    description=form.description.data)

        try:
            # add role to the database
            db.session.add(role)
            db.session.commit()
            flash('You have successfully added a new role.')
        except:
            # in case role name already exists
            flash('Error: role name already exists.')

        # redirect to the roles page
        return redirect(url_for('admin.list_roles'))

    # load role template
    return render_template('admin/roles/role.html', add_role=add_role,
                           form=form, title='Add Role')

@admin.route('/roles/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_role(id):
    """
    Edit a role
    """
    check_admin()

    add_role = False

    role = Role.query.get_or_404(id)
    form = RoleForm(obj=role)
    if form.validate_on_submit():
        role.name = form.name.data
        role.description = form.description.data
        db.session.add(role)
        db.session.commit()
        flash('You have successfully edited the role.')

        # redirect to the roles page
        return redirect(url_for('admin.list_roles'))

    form.description.data = role.description
    form.name.data = role.name
    return render_template('admin/roles/role.html', add_role=add_role,
                           form=form, title="Edit Role")

@admin.route('/roles/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_role(id):
    """
    Delete a role from the database
    """
    check_admin()

    role = Role.query.get_or_404(id)
    db.session.delete(role)
    db.session.commit()
    flash('You have successfully deleted the role.')

    # redirect to the roles page
    return redirect(url_for('admin.list_roles'))

    return render_template(title="Delete Role")


# Employee Views
@admin.route('/employees')
@login_required
def list_employees():
    """
    List all employees
    """
    check_admin()

    employees = Employee.query.all()
    return render_template('admin/employees/employees.html',
                           employees=employees, title='Employees')

@admin.route('/employees/assign/<int:id>', methods=['GET', 'POST'])
@login_required
def assign_employee(id):
    """
    Assign a department and a role to an employee
    """
    check_admin()

    employee = Employee.query.get_or_404(id)

    # prevent admin from being assigned a department or role
    # if employee.is_admin:
    #     abort(403)

    form = EmployeeAssignForm(obj=employee)
    if form.validate_on_submit():
        employee.email = form.email.data
        employee.first_name = form.first_name.data
        employee.last_name = form.last_name.data
        employee.department = form.department.data
        employee.role = form.role.data
        employee.is_admin = form.is_admin.data
        db.session.add(employee)
        db.session.commit()
        flash('You have successfully assigned a department and role.')

        # redirect to the roles page
        return redirect(url_for('admin.list_employees'))

    return render_template('admin/employees/employee.html',
                           employee=employee, form=form,
                           title='Assign Employee')

# Project Views
@admin.route('/projects')
@login_required
def list_projects():
    """
    List all projects
    """
    # check_admin()

    projects = Project.query.all()
    return render_template('admin/projects/projects.html',
                           projects=projects, title='Projects')

@admin.route('/projects/view/<int:id>', methods=['GET', 'POST'])
@login_required
def view_project(id):
    """
    View project detail
    """

    project = Project.query.get_or_404(id)
    return render_template('admin/projects/view_project.html',
                           project=project, title='Project')


@admin.route('/projects/add', methods=['GET', 'POST'])
@login_required
def add_project():
    """
    Add a role to the database
    """
    check_admin()

    add_project = True

    form = ProjectAssignForm()

    project_member = []
    for idx, member in enumerate(form.project_member.data):
        if member == None:
            project_member = project_member
        else:
            project_member.append(member['project_member'])
    
    if form.validate_on_submit():
        project = Project(name=form.name.data,
                          description=form.description.data,
                          status = form.status.data,
                          department = form.department.data,
                          employee = form.employee.data,
                          project_member = project_member
                          )



        try:
            # add role to the database
            db.session.add(project)
            db.session.commit()
            flash('You have successfully added a new project.')
        except:
            # in case role name already exists
            flash('Error: Project name already exists.')

        # redirect to the roles page
        return redirect(url_for('admin.list_projects'))

    # load role template
    return render_template('admin/projects/project.html', add_project=add_project,
                           form=form, title='Add Project')


@admin.route('/projects/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_project(id):
    """
    Edit a project
    """
    check_admin()
 
    # add_project = False  
    project = Project.query.get_or_404(id)

    form = ProjectAssignForm(obj=project)

    project_member = []
    for idx, member in enumerate(form.project_member.data):
        if member == None:
            project_member = project_member
        else:
            project_member.append(member['project_member'])
  

    if form.validate_on_submit():
        project.name = form.name.data
        project.description = form.description.data
        project.status= form.status.data
        project.department = form.department.data
        project.employee = form.employee.data
        project.start_date = form.start_date.data
        project.project_member = [x for x in project.project_member + project_member if x is not None]
        db.session.add(project)
        db.session.commit()
        # flash('{}'.format([x for x in project.project_member + project_member if x is not None]))
        # flash('{}'.format(project.project_member))
        # flash('{}'.format(project_member))
        flash('You have successfully edited the project.')
        return redirect(url_for('admin.list_projects'))
    return render_template('admin/projects/edit_project.html', project=project,
                           form=form, title="Edit project")


@admin.route('/projects/edit/<int:id>',methods=['GET', 'POST'])
def index():
    project = Project.query.first()
    form = ProjectAssignForm(obj = project)
    form.project_member.min_entries=1
    if form.validate_on_submit():
        form.populate_obj(project)
        db.session.commit()
    return render_template('admin/projects/project.html', form = form)

@admin.route('/projects/delete/<int:pid>/<int:mid>', methods=['GET', 'POST'])
@login_required
def delete_project_member(pid,mid):
    check_admin()

    project = Project.query.get_or_404(pid)
    member  = Employee.query.get_or_404(mid)
    project.project_member.remove(member)
    db.session.commit()

    # redirect to the edit project page
    return redirect(url_for('admin.edit_project',id=pid))

    return render_template(title="Delete Project")



@admin.route('/projects/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_project(id):
    """
    Delete a project member from the database
    """
    check_admin()

    project = Project.query.get_or_404(id)
    db.session.delete(project)
    db.session.commit()
    flash('You have successfully deleted the project.')

    # redirect to the roles page
    return redirect(url_for('admin.list_projects'))

    return render_template(title="Delete Project")




