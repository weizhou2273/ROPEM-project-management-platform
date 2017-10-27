# app/admin/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectMultipleField,SelectField,\
					TextAreaField,FormField, FieldList,RadioField,BooleanField,\
					DateField
from wtforms_components import DateTimeField
from wtforms.validators import DataRequired, Email, EqualTo

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
    email = StringField('Email', validators=[DataRequired(), Email()])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])

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
    def __init__(self, csrf_enabled=False, *args, **kwargs):
        super(EmployeeForm, self).__init__(csrf_enabled=False, *args, **kwargs)

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
    						min_entries=1,
    						model=Employee)
    start_date =  DateTimeField(
        'Start Date',
        # validators=[DateRange(
        #     min=datetime(2000, 1, 1),
        #     max=datetime(2099, 12, 31)
        # )]
        )