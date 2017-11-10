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
from ..models import Department, Role, Project, Employee, Tag, Permission 



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
    username = StringField('Username', validators=[DataRequired()])

    department = QuerySelectField(query_factory=lambda: Department.query.all(),
                                  get_label="name")
    role = QuerySelectField(query_factory=lambda: Role.query.all(),
                            get_label="name")
    

    permission = QuerySelectField(query_factory = lambda: Permission.query.all(),
                                 get_label = 'name', default = 'Viewer')

    submit = SubmitField('Submit')


class EmployeeForm(FlaskForm):
    project_member = QuerySelectField(query_factory=lambda: Employee.query.order_by(Employee.last_name),
                                   get_label=lambda employee: '{}, {} ({})'.format(employee.last_name,employee.first_name,employee.role),
                                   allow_blank=True)
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

class TagField(StringField):
    def _value(self):
        if self.data:
            # Display tags as a comma-separated list
            return ', '.join([tag.name for tag in self.data])
        return ''

    def get_tags_from_string(self, tag_string):
        raw_tags = tag_string.split(',')
        # Filter out any empty tag names.
        tag_names = [name.strip() for name in raw_tags if name.strip()]
        #Query the database and retrieve any tags we have already saved.
        existing_tags = Tag.query.filter(Tag.name.in_(tag_names))
        #Determine wichh tag names are new. 
        new_names = set(tag_names) - set([tag.name for tag in existing_tags])
        # Create a list of unsaved Tag instances for the new tags.
        new_tags = [Tag(name=name) for name in new_names]

        # return all the existing tags + all the new, unsaved tags.
        return list(existing_tags) + new_tags 

    def process_formdata(self, valuelist):
        if valuelist:
            self.data = self.get_tags_from_string(valuelist[0])
        else:
            self.data = []

class ProjectAssignForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    project_type = SelectField('Project type', choices=[('Ad-hoc','Ad-hoc'),
                                                  ('Recurrent','Recurrent') ],default=None)      
    project_phase = SelectField('Project phase', choices=[(i,i) for i in   
                                                   ('Conception','Planning','Development','Close')],
                                                   default=None)      
    department = QuerySelectField(query_factory=lambda: Department.query.all(),
                                   get_label= 'description',
                                   allow_blank=True)
    project_lead = QuerySelectField(query_factory=lambda: Employee.query.all(),
                                   get_label=lambda employee: '{}, {} ({})'.format(employee.last_name,employee.first_name,employee.role),
                                   allow_blank=True)


    members = ModelFieldList(FormField(EmployeeForm),
    						min_entries=1,
    						model=Employee)
    start_date = DateField('Project start date', format="%m/%d/%Y",validators=[DataRequired()])
    tags = TagField('Tags', description = 'Separate multiple tags with commas.')










    