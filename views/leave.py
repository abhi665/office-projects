from flask import Flask,request,jsonify
from models.employee import Employee
from models.leave import Leave_span,Leave_type,Leave_allotment,Leave_application
from flask_sqlalchemy import SQLAlchemy
from models.db import Database
from flasgger.utils import swag_from
from help.jwtdecorater import token_required
from sqlalchemy.dialects.postgresql import UUID
from datetime import date

class Leave:
    @token_required
    @swag_from("../swagger/leavespan.yml")
    def leave_span():
        from_date = request.form.get('from_date')
        to_date = request.form.get('to_date')
        from_time = request.form.get('from_time')
        to_time = request.form.get('to_time')
        if to_date == from_date:
            if from_time == 'PM' and to_time == "AM":
                return jsonify({"message":"entered data not valid"}), 404
        leave_span = Leave_span(from_date,to_date,from_time,to_time)
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
    @swag_from("../swagger/addleaveallot.yml") 
    def addleave_allotment():
        employee_id = request.form.get('employee_id')
        alloted_leave = request.form.get('alloted_leave')
        Leave_allotmentdata = Leave_allotment.query.with_entities(Leave_allotment.employee_id).all()
        empid = []
        for item in Leave_allotmentdata:
            empid.append(str(item.employee_id))
        if employee_id in empid:
            return jsonify({"message":"Sir you are not new employee"}), 404
        leave_allotment_obj = Leave_allotment(employee_id,int(alloted_leave)) 
        Database.db().session.add(leave_allotment_obj)
        Database.db().session.commit()
        Database.db().session.flush()
        return jsonify({"leave_allotment_id":leave_allotment_obj.id,"message":"success"})

    @token_required
    @swag_from("../swagger/addleaveapplication.yml")
    def leave_application():
        try:
            employee_id = request.form.get('employee_id')
            leave_span_id = request.form.get('leave_span_id')
            leave_type_id = request.form.get('leave_type_id')
            description = request.form.get('description')
            leavespandata = Leave_span.query.filter_by(id = leave_span_id).first()
            if leavespandata.to_date == leavespandata.from_date and leavespandata.from_time==leavespandata.to_time :
                leave_days = 0.5
            elif leavespandata.to_date == leavespandata.from_date and leavespandata.from_time!=leavespandata.to_time :
                leave_days = 1
            elif leavespandata.from_time == "AM" and leavespandata.to_time == "AM":
                leave = leavespandata.to_date - leavespandata.from_date
                leave = float(leave.days)+0.5
                leave_days = leave
            elif leavespandata.from_time == "PM" and leavespandata.to_time == "AM":
                leave = leavespandata.to_date - leavespandata.from_date
                leave = float(leave.days)-0.5
                leave_days = leave
            else:
                leave = leavespandata.to_date - leavespandata.from_date
                leave_days = float(leave.days) + 1
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
        except:
            return jsonify({'message':'unexcepted error'}), 404

    @token_required
    @swag_from("../swagger/resetleaveallotment.yml")
    def leave_allotment_reset():
        # if "01-01" == str(date.today())[5:]:
        Leave_allotment.reset()
        return jsonify({"message":"success"})
        

    @token_required
    @swag_from("../swagger/leaveapprovment.yml")
    def Leave_approvement():
        Leave_application_id = request.form.get("Leave_application_id")
        Leave_allotment_id = request.form.get("Leave_allotment_id")
        approval = request.form.get("approval")
        Leave_allotmentdata = Leave_allotment.query.filter_by(id = Leave_allotment_id).first()
        Leave_applicationData = Leave_application.getdatabyid(Leave_application_id)
        if approval == "yes":
            leave_status = "approved"
            Leave_application.leave_status_update(Leave_applicationData.id,leave_status)            
            leave_left = (Leave_allotmentdata.alloted_leave - Leave_applicationData.leave_days)
            Leave_allotment.update(Leave_allotmentdata.id,leave_left)
            return jsonify({"message":"success"})
        leave_status = "rejected"
        Leave_application.leave_status_update(Leave_applicationData.id,leave_status)
        return jsonify({"message":"no approval"})  

    @token_required
    @swag_from("../swagger/leaveapplication.yml")
    def get_leavelist():
        find = request.args.get('find')
        status = request.args.get('status')
        leave_application =  Leave_application.getlistapplication(find,status)
        leave_list = []
        for item in leave_application:
            empdata = Employee.getempbyID(item.employee_id)
            leavespandata = Leave_span.query.filter_by(id = item.leave_span_id).first()
            leavetypedata = Leave_type.query.filter_by(id = item.leave_type_id).first()
            leave_list.append({
                'id':item.id,
                'leave_allotment_id':item.leave_allotment_id,
                'employee_id':item.employee_id,
                'employee_code':empdata.employee_code,
                'first_name':empdata.first_name,
                'last_name':empdata.last_name,
                'leave_span_id':item.leave_span_id,
                'from_date':leavespandata.from_date,
                'from_time':leavespandata.from_time,
                'to_date':leavespandata.to_date,
                'to_time':leavespandata.to_time,
                'leave_type_id':item.leave_type_id,
                'leave_type':leavetypedata.leave_type,
                'description':item.description,
                'leave_days':"{:.2f}".format(item.leave_days),
                # 'leave_days':leave,
                'leave_status':item.leave_status,
            })
        return jsonify(leave_list)    

    @token_required
    @swag_from("../swagger/leaveallotment.yml")
    def get_listallotement():
        find = request.args.get('find')
        leave_allotment =  Leave_allotment.getlistallotement(find)
        leave_alloted_list = []
        for item in leave_allotment:
            empdata = Employee.getempbyID(item.employee_id)
            leave_alloted_list.append({
                'id':item.id,
                'employee_id':item.employee_id,
                'employee_code':empdata.employee_code,
                'first_name':empdata.first_name,
                'last_name':empdata.last_name,
                'alloted_leave': "{:.2f}".format(item.alloted_leave),
            })
        return jsonify(leave_alloted_list)

    @token_required
    def delete_leavespan(leave_span_id):
        del_leavespan = Leave_span.query.filter_by(id=leave_span_id).first()
        if del_leavespan:
            Leave_span.delete(del_leavespan)
            return ("sucessfully deleted")
        return ("unsucessful"), 404

    @token_required
    def delete_leavetype(leave_type_id):
        del_leavetype = Leave_type.query.filter_by(id=leave_type_id).first()
        if del_leavetype:
            Leave_type.delete(del_leavetype)
            return ("sucessfully deleted")
        return ("unsucessful"), 404

    @token_required
    def delete_leaveallotment(employee_id):
        del_leaveallot = Leave_allotment.query.filter_by(employee_id=employee_id).first()
        if del_leaveallot:
            Leave_allotment.delete(del_leaveallot)
            return ("sucessfully deleted")
        return ("unsucessful"), 404