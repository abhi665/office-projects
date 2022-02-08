from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from datetime import date
from sqlalchemy import null
from sqlalchemy.sql.sqltypes import String
from models.employee import Employee
import uuid
from sqlalchemy.dialects.postgresql import UUID

db = SQLAlchemy()

class Leave_span(db.Model):
    __tablename__ = 'leave_span'
    id = db.Column(UUID(as_uuid=True), primary_key=True,default=uuid.uuid4)
    from_date = db.Column(db.Date())
    to_date = db.Column(db.Date())
    def __init__(self,from_date,to_date):
        self.from_date = from_date,
        self.to_date = to_date


class Leave_type(db.Model):
    __tablename__ = 'leave_type'
    id = db.Column(UUID(as_uuid=True), primary_key=True,default=uuid.uuid4)
    leave_type = db.Column(db.String(25))
    def __init__(self,leave_type):
        self.leave_type = leave_type
        
    
class Leave_allotment(db.Model):
    __tablename__ = 'leave_allotment'
    id = db.Column(UUID(as_uuid=True), primary_key=True,default=uuid.uuid4)
    employee_id = db.Column(UUID(as_uuid=True),db.ForeignKey(Employee.employee_id))
    leave_span_id = db.Column(UUID(as_uuid=True),db.ForeignKey('leave_span.id'))
    leave_type_id = db.Column(UUID(as_uuid=True),db.ForeignKey('leave_type.id'))
    alloted_leave = db.Column(db.Integer)

    def __init__(self,employee_id,leave_span_id=null,leave_type_id=null,alloted_leave=15):
        self.employee_id = employee_id
        self.leave_span_id = leave_span_id
        self.leave_type_id = leave_type_id
        self.alloted_leave = alloted_leave
    def update(id,leave_left):
        Leave_allotment.query.filter_by(id = id).update(dict(alloted_leave = leave_left))
        db.session.commit()
    def reset(id):
        Leave_allotment.query.filter_by(employee_id = id).update(dict(alloted_leave = 15))
        db.session.commit()
    def getlistallotement():
        leaveallotedlist = Leave_allotment.query.all()
        return leaveallotedlist


class Leave_application(db.Model):
    __tablename__= 'leave_application'
    id = db.Column(UUID(as_uuid=True), primary_key=True,default=uuid.uuid4)
    leave_allotment_id = db.Column(UUID(as_uuid=True),db.ForeignKey('leave_allotment.id'))
    employee_id = db.Column(UUID(as_uuid=True),db.ForeignKey(Employee.employee_id))
    leave_span_id = db.Column(UUID(as_uuid=True),db.ForeignKey('leave_span.id'))
    leave_type_id = db.Column(UUID(as_uuid=True),db.ForeignKey('leave_type.id'))
    description= db.Column(db.String())
    leave_days = db.Column(db.String())
    leave_status = db.Column(db.String())
    
    def __init__(self,leave_allotment_id,employee_id,leave_span_id,leave_type_id,description,leave_days=0,leave_status=""):
        self.leave_allotment_id = leave_allotment_id
        self.employee_id = employee_id
        self.leave_span_id = leave_span_id
        self.leave_type_id = leave_type_id
        self.description = description
        self.leave_days = leave_days
        self.leave_status = leave_status
    def update(id,leave_days):
        Leave_application.query.filter_by(id = id).update(dict(leave_days = leave_days))
        db.session.commit()    
    def leave_status_update(id,leave_status):
         Leave_application.query.filter_by(id = id).update(dict(leave_status = leave_status))
         db.session.commit()
# class Leave_approvement(db.Model):
#     __tablename__= 'Leave_approvement' 
#     id = db.Column(UUID(as_uuid=True), primary_key=True,default=uuid.uuid4)

    def getlistapplication():
        leavelist = Leave_application.query.all()
        return leavelist
