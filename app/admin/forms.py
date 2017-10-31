# app/admin/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectMultipleField,SelectField,\
					TextAreaField,FormField, FieldList,RadioField,BooleanField,\
					DateField,validators
from wtforms_components import DateTimeField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms_alchemy.fields import QuerySelectMultipleField
from wtforms_alchemy import ModelForm, ModelFieldList
from wtforms import widgets
from wtforms.fields import FormField
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
    project_member = QuerySelectField(query_factory=lambda: Employee.query.order_by(Employee.last_name),
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
    name = StringField('Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    status = SelectField('status', choices=[('Completed','Completed'),('In progress','In progress')])
    department = QuerySelectField(query_factory=lambda: Department.query.all(),
                                   get_label="name")
    employee = QuerySelectField(query_factory=lambda: Employee.query.all(),
                                   get_label="last_name")
    members = ModelFieldList(FormField(EmployeeForm),
    						min_entries=1,
    						model=Employee)
    start_date = DateField('Pick a Date', format="%m/%d/%Y", validators=[DataRequired()])
    