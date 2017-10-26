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
    is_admin = BooleanField('is_admin',default=False)
    submit = SubmitField('Submit')

class EmployeeForm(FlaskForm):
    # Last_Name = SelectField('Last_Name',validators = [DataRequired()], #coerce=int,
    #     choices = [x.name for x in Role.query.all() ])
    # role = QuerySelectField(query_factory=lambda: Role.query.all(),
    #                                get_label="name",
    #                                allow_blank=True)
    # project_lists = SelectField('Member',
    # 							choices = [(e.id,e.last_name) for e in Employee.query.all()]
    #                                )

    project_lists = QuerySelectField(query_factory=lambda: Employee.query.order_by(Employee.last_name),
                                   get_label="last_name",
                                   allow_blank=True
                                   )

class ModelFieldList(FieldList):
    def __init__(self, *args, **kwargs):         
        self.model = kwargs.pop("model", None)
        super(ModelFieldList, self).__init__(*args, **kwargs)
        if not self.model:
            raise ValueError("ModelFieldList requires model to be set")

    def populate_obj(self, obj, name):
        while len(getattr(obj, name)) < len(self.entries):
            newModel = self.model()
            db.session.add(newModel)
            getattr(obj, name).append(newModel)
        while len(getattr(obj, name)) > len(self.entries):
            db.session.delete(getattr(obj, name).pop())
        super(ModelFieldList, self).populate_obj(obj, name)

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
    member = ModelFieldList(FormField(EmployeeForm),
    						min_entries=3,
    						model=Employee)

    # member = QuerySelectMultipleField(query_factory=lambda: Employee.query.all(),
	   #                                get_pk = lambda e: e.id,
	   #                                get_label = lambda e: e.first_name + ' ' +e.last_name,
	   #                                option_widget = widgets.CheckboxInput(),
	   #                                widget = widgets.ListWidget(prefix_label=False))


