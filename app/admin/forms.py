# app/admin/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectMultipleField,SelectField,\
					TextAreaField,FormField, FieldList,RadioField,BooleanField
from wtforms.validators import DataRequired
from wtforms.ext.sqlalchemy.fields import QuerySelectField#,QuerySelectMultipleField
from wtforms_alchemy.fields import QuerySelectMultipleField
from wtforms_alchemy import ModelForm, ModelFieldList
from wtforms import widgets
# from flask.ext.wtf import Form
from wtforms.fields import FormField

import wtforms as wtf,validators
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
    administrator = BooleanField('Administrator',default=False)
    submit = SubmitField('Submit')

class EmployeeForm(FlaskForm):
    # Last_Name = SelectField('Last_Name',validators = [DataRequired()], #coerce=int,
    #     choices = [x.name for x in Role.query.all() ])
    Last_Name = QuerySelectField(query_factory=lambda: Employee.query.all(),
                                   get_label="last_name",allow_blank=True)


class ProjectAssignForm(FlaskForm):
    """
    Form for admin to assign departments and roles to projects
    """

    name = StringField('Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    status = SelectField('status', choices=[('Completed','Completed'),('In progress','In progress')])
    department = QuerySelectField(query_factory=lambda: Department.query.all(),
                                   get_label="name")
    employee = QuerySelectField(query_factory=lambda: Employee.query.all(),
                                   get_label="last_name")

    project_member = FieldList(FormField(EmployeeForm), min_entries=2)
    # project_member = QuerySelectMultipleField(query_factory=lambda: Employee.query.all(),
    #                                get_pk = lambda e: e.id,
    #                                get_label = lambda e: e.first_name + ' ' +e.last_name,
    #                                option_widget = widgets.CheckboxInput(),
    #                                widget = widgets.ListWidget(prefix_label=False))


   

    submit = SubmitField('Submit')