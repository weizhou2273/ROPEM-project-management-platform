# app/admin/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectMultipleField,SelectField
from wtforms.validators import DataRequired
from wtforms.ext.sqlalchemy.fields import QuerySelectField,QuerySelectMultipleField
from ..models import Department, Role, Project, Employee



class DepartmentForm(FlaskForm):
    """
    Form for admin to add or edit a department
    """
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit') 

class RoleForm(FlaskForm):
    """
    Form for admin to add or edit a role
    """
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')


class EmployeeAssignForm(FlaskForm):
    """
    Form for admin to assign departments and roles to employees
    """
    department = QuerySelectField(query_factory=lambda: Department.query.all(),
                                  get_label="name")
    role = QuerySelectField(query_factory=lambda: Role.query.all(),
                            get_label="name")
    submit = SubmitField('Submit')



class ProjectAssignForm(FlaskForm):
    """
    Form for admin to assign departments and roles to projects
    """
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    department = QuerySelectField(query_factory=lambda: Department.query.all(),
                                  get_label="name")
    # role = QuerySelectField(query_factory=lambda: Role.query.all(),
    #                         get_label="name")
    # project_leader = QuerySelectField(query_factory=lambda: Employee.query.all(),
			 #                            get_label="last_name")
    # Project_member = QuerySelectMultipleField(query_factory=lambda: Employee.query.all(),
    # 									allow_blank=True,
			 #                            get_label="last_name")
    # employee = SelectMultipleField(u'Programming Language', 
    # 								 choices=[('cpp', 'C++'), ('py', 'Python'), ('text', 'Plain Text')],
    # 								 option_widget = True)


    submit = SubmitField('Submit')