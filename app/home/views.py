# app/home/views.py

# update imports
from flask import abort, render_template
from flask_login import current_user, login_required
from ..models import Department,Role,Employee,Project
from . import home

@home.route('/')
def homepage():
    """
    Render the homepage template on the / route
    """
    projects = Project.query.all()

    return render_template('home/index.html',
                            projects=projects,
                            title="Welcome")

@home.route('/dashboard')
@login_required
def dashboard():
    """
    Render the dashboard template on the /dashboard route
    """
    employee = Employee.query.get_or_404(current_user.id)
    projects = Project.query.filter(Project.project_lead_id==employee.id).all()
    join_projects = Project.query.filter(Project.project_member.contains(employee)).all()
    return render_template('home/dashboard.html',
                           projects=projects, 
                           employee = employee, 
                           join_projects = join_projects,
                           title='Projects')

# add admin dashboard view
@home.route('/admin/dashboard')
@login_required
def admin_dashboard():
    # prevent non-admins from accessing the page
    if not current_user.permission.name == 'Admin':
        abort(403)
    employee = Employee.query.get_or_404(current_user.id)
    projects = Project.query.filter(Project.project_lead_id==employee.id).all()
    join_projects = Project.query.filter(Project.project_member.contains(employee)).all()
    return render_template('home/admin_dashboard.html',
                           projects=projects, 
                           employee = employee, 
                           join_projects = join_projects,
                           title='Projects')


