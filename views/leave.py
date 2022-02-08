from flask import Flask,request,jsonify
from models.employee import Employee
from models.leave import Leave_span,Leave_type,Leave_allotment,Leave_application
from flask_sqlalchemy import SQLAlchemy
from models.db import Database
from flasgger.utils import swag_from
from help.jwtdecorater import token_required
from sqlalchemy.dialects.postgresql import UUID

class Leave:
    @token_required
    @swag_from("../swagger/leavespan.yml")
    def leave_span():
        from_date = request.form.get('from_date')
        to_date = request.form.get('to_date')
        leave_span = Leave_span(from_date,to_date)
        Database.db().session.add(leave_span)
        Database.db().session.commit()
        Database.db().session.flush()
        return jsonify({"leave_span_id":leave_span.id,"message":"success"})

    @token_required
    @swag_from("../swagger/leavetype.yml")    
    def leave_type():
        leave_type = request.form.get('leave_type')
        leave_type = Leave_type(leave_type)
        Database.db().session.add(leave_type)
        Database.db().session.commit()
        Database.db().session.flush()
        return jsonify({"leave_type_id":leave_type.id,"message":"success"})

    @token_required
    def addleave_allotment():
        employee_id = request.form.get('employee_id')
        leave_span_id = request.form.get('leave_span_id')
        leave_type_id = request.form.get('leave_type_id')
        alloted_leave = request.form.get('alloted_leave')
        Leave_allotmentdata = Leave_allotment.query.with_entities(Leave_allotment.employee_id).all()
        empid = []
        for item in Leave_allotmentdata:
            empid.append(str(item.employee_id))
        if employee_id in empid:
            return jsonify({"message":"Sir you are not new employee"}), 404
        leave_allotment_obj = Leave_allotment(employee_id,leave_span_id,leave_type_id,int(alloted_leave)) 
        Database.db().session.add(leave_allotment_obj)
        Database.db().session.commit()
        Database.db().session.flush()
        return jsonify({"leave_allotment_id":leave_allotment_obj.id,"message":"success"})

    @token_required
    @swag_from("../swagger/leaveapplication.yml")
    def leave_application():
        # try:
            employee_id = request.form.get('employee_id')
            leave_span_id = request.form.get('leave_span_id')
            leave_type_id = request.form.get('leave_type_id')
            description = request.form.get('description')
            leave_days = request.form.get('leave_days')
            Leave_allotmentdata = Leave_allotment.query.filter_by(employee_id = employee_id).first()
            leave_allotment_id = Leave_allotmentdata.id
            if int(leave_days) <= Leave_allotmentdata.alloted_leave:
                leave_status = "pending"
                leave_application_obj = Leave_application(leave_allotment_id,employee_id,leave_span_id,leave_type_id,description,leave_days,leave_status)
                Database.db().session.add(leave_application_obj)
                Database.db().session.commit()
                Database.db().session.flush()
                return jsonify({"leave_application_id":leave_application_obj.id,"message":"success"})
            return jsonify({"message":"no leaves left"}), 404
        # except:
        #     return jsonify({'message':'unexcepted error'}), 404

    # @token_required
    # @swag_from("../swagger/leaveallotment.yml")
    # def leave_allotment(employee_id):
    #     leave_days = request.form.get('leave_days')
    #     Leave_allotmentdata = Leave_allotment.query.filter_by(employee_id = employee_id).first()
    #     Leave_applicationData = Leave_application.query.filter_by(leave_allotment_id = Leave_allotmentdata.id).first()
    #     if int(leave_days) <= Leave_allotmentdata.alloted_leave:
    #         leave_status = "pending"
    #         Leave_application.leave_status_update(Leave_applicationData.id,leave_status)            
    #         return jsonify({"leave_days":leave_days,
    #                         "message":"success"})
    #     return jsonify({"message":"no leaves"})

    @token_required
    def leave_allotment_reset(employee_id):
        Leave_allotment.reset(employee_id)
        return jsonify({"message":"success"})

    @token_required
    @swag_from("../swagger/leaveapprovment.yml")
    def Leave_approvement():
        Leave_application_id = request.form.get("leave_application_id")
        Leave_allotment_id = request.form.get("Leave_allotment_id")
        approval = request.form.get("approval")
        Leave_allotmentdata = Leave_allotment.query.filter_by(id = Leave_allotment_id).first()
        Leave_applicationData = Leave_application.query.filter_by(id = Leave_application_id).first()
        if approval == "yes":
            leave_status = "approved"
            Leave_application.leave_status_update(Leave_applicationData.id,leave_status)            
            leave_left = (Leave_allotmentdata.alloted_leave - int(Leave_applicationData.leave_days))
            print(Leave_allotmentdata.id)
            Leave_allotment.update(Leave_allotmentdata.id,leave_left)
            return jsonify({"message":"success"})
        leave_status = "rejected"
        Leave_application.leave_status_update(Leave_applicationData.id,leave_status)    
        return jsonify({"message":"no approval"})  

    @token_required
    @swag_from("../swagger/leaveapplication.yml")
    def get_leavelist():
        leave_application =  Leave_application.getlistapplication()
        leave_list = []
        for item in leave_application:
            leave_list.append({
                'id':item.id,
                'leave_allotment_id':item.leave_allotment_id,
                'description':item.description,
                'leave_days':item.leave_days,
                'leave_status':item.leave_status,
            })
        return jsonify(leave_list)    

    @token_required
    @swag_from("../swagger/leaveapplication.yml")
    def get_listallotement():
        leave_allotment =  Leave_allotment.getlistallotement()     
        leave_alloted_list = []
        for item in leave_allotment:
            leave_alloted_list.append({
                'id':item.id,
                'employee_id':item.employee_id,
                'leave_span_id':item.leave_span_id,
                'leave_type_id':item.leave_type_id,
                'alloted_leave':item.alloted_leave,
            })
        return jsonify(leave_alloted_list)
