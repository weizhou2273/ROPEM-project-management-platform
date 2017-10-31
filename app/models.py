# app/models.py

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from app import db, login_manager

subs = db.Table('subs',
    db.Column('project_id',db.Integer,db.ForeignKey('projects.id', ondelete='cascade')),
    db.Column('member_id',db.Integer,db.ForeignKey('employees.id', ondelete='cascade')),
    db.UniqueConstraint('project_id','member_id',name = 'member_project_id'),
    )


class Employee(UserMixin, db.Model):
    """
    Create an Employee table
    """

    # Ensures table will be named in plural and not in singular
    # as is the name of the model
    __tablename__ = 'employees'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), index=True, unique=True)
    username = db.Column(db.String(60), index=True, unique=True)
    first_name = db.Column(db.String(60), index=True)
    last_name = db.Column(db.String(60), index=True)
    password_hash = db.Column(db.String(128))
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    is_admin = db.Column(db.Boolean, default=False)
    projects = db.relationship('Project',backref='employee',
                                lazy ='dynamic')
    projects_list = db.relationship('Project',backref='member',lazy='dynamic')
    # project_list= db.relationship('Project',secondary=subs,backref=db.backref('member',lazy='dynamic')
    #                                         # cascade='delete-orphan',
    #                                         # single_parent=False
    #                                         )
    @property
    def password(self):
        """
        Prevent pasword from being accessed
        """
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        """
        Set password to a hashed password
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        Check if hashed password matches actual password
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '{}'.format(self.username)

# Set up user_loader
@login_manager.user_loader
def load_user(user_id):
    return Employee.query.get(int(user_id))

class Department(db.Model):
    """
    Create a Department table
    """

    __tablename__ = 'departments'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    employees = db.relationship('Employee', backref='department',
                                lazy='dynamic')
    projects = db.relationship('Project',backref='department',
                                lazy ='dynamic')
    def __repr__(self):
        return '<Department: {}>'.format(self.name)

class Role(db.Model):
    """
    Create a Role table
    """

    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    employees = db.relationship('Employee', backref='role',
                                lazy='dynamic')

    def __repr__(self):
        return '<Role: {}>'.format(self.name)

class Project(db.Model):
    """
    Create a project table
    """
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    status = db.Column(db.String(200))
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    project_lead_id = db.Column(db.Integer, db.ForeignKey('employees.id'))
    project_member= db.relationship('Employee',
                                    secondary=subs,
                                    backref=db.backref('project_lists',lazy='dynamic'),
                                    # cascade='delete-orphan',
                                    single_parent=True
                                               )
    start_date = db.Column(db.DateTime, nullable=True)
    def __repr__(self):
        return '<Project: {}>'.format(self.name)



