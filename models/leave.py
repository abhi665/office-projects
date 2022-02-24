from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from datetime import date
from sqlalchemy import null
from sqlalchemy.sql.sqltypes import String
from models.employee import Employee
import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import or_,and_

db = SQLAlchemy()

class Leave_span(db.Model):
    __tablename__ = 'leave_span'
    id = db.Column(UUID(as_uuid=True), primary_key=True,default=uuid.uuid4)
    from_date = db.Column(db.Date())
    to_date = db.Column(db.Date())
    from_time = db.Column(db.String(25))
    to_time = db.Column(db.String(25))
    def __init__(self,from_date,to_date,from_time,to_time):
        self.from_date = from_date,
        self.to_date = to_date,
        self.from_time = from_time,
        self.to_time = to_time

    def delete(del_leavespan):
        db.session.delete(del_leavespan)
        db.session.commit()


class Leave_type(db.Model):
    __tablename__ = 'leave_type'
    id = db.Column(UUID(as_uuid=True), primary_key=True,default=uuid.uuid4)
    leave_type = db.Column(db.String(25))
    def __init__(self,leave_type):
        self.leave_type = leave_type
        
    def delete(del_leavetype):
        db.session.delete(del_leavetype)
        db.session.commit()
        
    
class Leave_allotment(db.Model):
    __tablename__ = 'leave_allotment'
    id = db.Column(UUID(as_uuid=True), primary_key=True,default=uuid.uuid4)
    employee_id = db.Column(UUID(as_uuid=True),db.ForeignKey(Employee.employee_id))
    alloted_leave = db.Column(db.Float(4,2))

    def __init__(self,employee_id,alloted_leave=15):
        self.employee_id = employee_id
        self.alloted_leave = alloted_leave
    def update(id,leave_left):
        Leave_allotment.query.filter_by(id = id).update(dict(alloted_leave = leave_left))
        db.session.commit()
    def reset():
        Leave_allotment.query.update(dict(alloted_leave = 15))
        db.session.commit()
    def getlistallotement(find):
        if find==None:
            leaveallotedlist = Leave_allotment.query.all()
            return leaveallotedlist
        else:
            leaveallotedlist = Leave_allotment.query.filter(or_(Leave_allotment.id == find,Leave_allotment.employee_id == find)).all()
            return leaveallotedlist
    def delete(del_leaveallot):
        db.session.delete(del_leaveallot)
        db.session.commit()


class Leave_application(db.Model):
    __tablename__= 'leave_application'
    id = db.Column(UUID(as_uuid=True), primary_key=True,default=uuid.uuid4)
    leave_allotment_id = db.Column(UUID(as_uuid=True),db.ForeignKey('leave_allotment.id'))
    employee_id = db.Column(UUID(as_uuid=True),db.ForeignKey(Employee.employee_id))
    leave_span_id = db.Column(UUID(as_uuid=True),db.ForeignKey('leave_span.id'))
    leave_type_id = db.Column(UUID(as_uuid=True),db.ForeignKey('leave_type.id'))
    description= db.Column(db.String())
    leave_days = db.Column(db.Float(4,2))
    leave_status = db.Column(db.String())
    
    def __init__(self,leave_allotment_id,employee_id,leave_span_id,leave_type_id,description,leave_days=0,leave_status=""):
        self.leave_allotment_id = leave_allotment_id
        self.employee_id = employee_id
        self.leave_span_id = leave_span_id
        self.leave_type_id = leave_type_id
        self.description = description
        self.leave_days = leave_days
        self.leave_status = leave_status
    def getdatabyid(id):
        leavedata = Leave_application.query.filter_by(id = id).first()
        return leavedata
    def update(id,leave_days):
        Leave_application.query.filter_by(id = id).update(dict(leave_days = leave_days))
        db.session.commit()    
    def leave_status_update(id,leave_status):
         Leave_application.query.filter_by(id = id).update(dict(leave_status = leave_status))
         db.session.commit()
# class Leave_approvement(db.Model):
#     __tablename__= 'Leave_approvement' 
#     id = db.Column(UUID(as_uuid=True), primary_key=True,default=uuid.uuid4)

    def getlistapplication(find,status):
        if find == '':
            find = None
        if status == '':
            status = None
        if find==None and status == None:
            leavelist = Leave_application.query.order_by(Leave_application.id.desc()).all()
            return leavelist
        elif find!=None and status == None:
            leavelist = Leave_application.query.filter(or_(Leave_application.id == find,Leave_application.employee_id == find,Leave_application.leave_span_id == find,Leave_application.leave_type_id == find)).order_by(Leave_application.id.desc()).all()
            return leavelist
        elif find==None and status != None:
            leavelist = Leave_application.query.filter(Leave_application.leave_status == status).all()
            return leavelist
        else:
            leavelist = Leave_application.query.filter(or_(Leave_application.id == find,Leave_application.employee_id == find,Leave_application.leave_span_id == find,Leave_application.leave_type_id == find),and_(Leave_application.leave_status == status)).order_by(Leave_application.id.desc()).all()
            return leavelist
