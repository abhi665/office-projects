from operator import or_
from typing import NewType
from flask_sqlalchemy import SQLAlchemy
import uuid
from sqlalchemy.dialects.postgresql import UUID
from models.country import Country
from sqlalchemy.sql import or_

db = SQLAlchemy()


class Employee(db.Model):

    __tablename__ = 'employees'

    employee_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    country_id = db.Column(UUID(as_uuid=True), db.ForeignKey(Country.country_id))
    employee_code = db.Column(db.String())
    first_name = db.Column(db.String())
    last_name = db.Column(db.String())
    employee_role = db.Column(db.String())
    email = db.Column(db.String())
    phno = db.Column(db.String())
    password = db.Column(db.String())
    gender = db.Column(db.String())
    otp = db.Column(db.String())

    def __init__(self, country_id, employee_code, first_name, last_name, employee_role, email, phno, password, gender, otp=''):
        self.country_id = country_id
        self.employee_code = employee_code
        self.first_name = first_name
        self.last_name = last_name
        self.employee_role = employee_role
        self.email = email
        self.phno = phno
        self.password = password
        self.gender = gender
        self.otp = otp
    def getallemp():
        employeelist=Employee.query.all()
        return employeelist

    def getlistemp(search, lower, upper):
        if search == None or len(search) == 0:
            employeelist = list(Employee.query.order_by(Employee.employee_id.desc()).limit(upper).all())
            return employeelist[int(lower):]
        else:
            employeelist = list(Employee.query.filter(or_(Employee.employee_code == search, Employee.email == search, Employee.phno == search, Employee.first_name.like("{}%".format(search)))))
            
            return employeelist
        #  with_entities(Employee.employee_code, Employee.email, Employee.phno)

    def getempbyID(employee_id):
        employee = Employee.query.filter_by(employee_id=employee_id).first()
        return employee

    def getempbycode(employee_code):
        employee = Employee.query.filter_by(employee_code=employee_code).first()
        return employee

    def addotp(employee_id, otp):
        otp = Employee.query.filter_by(employee_id=employee_id).update(dict(otp=otp))
        db.session.commit()

    def updatepass(employee_id, password):
        password = Employee.query.filter_by(employee_id=employee_id).update(dict(password=password))
        db.session.commit()

    def updateemp(employee_id, country_id=None, first_name=None, last_name=None, employee_role=None, email=None, phno=None, gender=None):
        if country_id != None:
            country_id = Employee.query.filter_by(employee_id=employee_id).update(dict(country_id=country_id))
        if first_name != None:
            first_name = Employee.query.filter_by(employee_id=employee_id).update(dict(first_name=first_name))
        if last_name != None:
            last_name = Employee.query.filter_by(employee_id=employee_id).update(dict(last_name=last_name))
        if employee_role != None:
            employee_role = Employee.query.filter_by(employee_id=employee_id).update(dict(employee_role=employee_role))
        if email != None:
            email = Employee.query.filter_by(employee_id=employee_id).update(dict(email=email))
        if phno != None:
            phno = Employee.query.filter_by(employee_id=employee_id).update(dict(phno=phno))
        if gender !=None:
            gender = Employee.query.filter_by(employee_id=employee_id).update(dict(gender=gender))
        db.session.commit()

    def updateempHr(employee_id,employee_code=None ,country_id=None, first_name=None, last_name=None, employee_role=None, email=None, phno=None, gender=None):
        if employee_code != None:
            employee_code = Employee.query.filter_by(employee_id=employee_id).update(dict(employee_code=employee_code))
        if country_id != None:
            country_id = Employee.query.filter_by(employee_id=employee_id).update(dict(country_id=country_id))
        if first_name != None:
            first_name = Employee.query.filter_by(employee_id=employee_id).update(dict(first_name=first_name))
        if last_name != None:
            last_name = Employee.query.filter_by(employee_id=employee_id).update(dict(last_name=last_name))
        if employee_role != None:
            employee_role = Employee.query.filter_by(employee_id=employee_id).update(dict(employee_role=employee_role))
        if email != None:
            email = Employee.query.filter_by(employee_id=employee_id).update(dict(email=email))
        if phno != None:
            phno = Employee.query.filter_by(employee_id=employee_id).update(dict(phno=phno))
        if gender!=None:
            gender = Employee.query.filter_by(employee_id=employee_id).update(dict(gender=gender))
        db.session.commit()

    def delete(employee):
        db.session.delete(employee)
        db.session.commit()
