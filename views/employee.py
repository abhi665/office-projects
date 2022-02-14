from flask import request, jsonify, make_response
import jwt
from models.employee import Employee
from models.country import Country
from sendotp import SendOtp
import hashlib
from models.db import Database
from datetime import datetime, timedelta
from help.jwtdecorater import token_required
from flasgger.utils import swag_from
import re
db = Database.db()

SECRET_KEY = "SECRATE"
TIME_JWT = 1440


class Employeeview:
    @token_required
    @swag_from("../swagger/swagger_create_employee.yml")
    def create_emp():
        try:
            token = request.headers['x-access-token']
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            if data['employee_role'] == "hr":
                country_name = request.form.get('country_name').lower()
                first_name = request.form.get("first_name").lower()
                last_name = request.form.get("last_name").lower()
                employee_role = request.form.get('employee_role').lower()
                employee_code = request.form.get('employee_code').lower()
                email = request.form.get('email').lower()
                phno = request.form.get('phno').lower()
                password = request.form.get('password').lower()
                password2 = request.form.get('password2').lower()
                gender = request.form.get('gender').lower()
                countries = Country.query.filter_by(country_name=country_name).first()
                employeelst = Employee.getallemp()
                emp_codelst = []
                emp_phlist = []
                emp_emaillist = []
                for item in employeelst:
                    emp_codelst.append(item.employee_code)
                    emp_phlist.append(item.phno)
                    emp_emaillist.append(item.email)
                if employee_code in emp_codelst:
                    return jsonify({'message': 'emp_code exists'}), 400
                if phno in emp_phlist:
                    return jsonify({'message': 'ph no existes'}), 400
                if email in emp_emaillist:
                    return jsonify({'message': 'email no existes'}), 400
                if password != password2:
                    return jsonify({'message': 'password not match'}), 400

                password = hashlib.md5(password.encode()).hexdigest()
                employees = Employee(countries.country_id, employee_code, first_name,
                                     last_name, employee_role, email, phno, password, gender, '')
                Database.db().session.add(employees)
                Database.db().session.commit()
                Database.db().session.flush()
                return jsonify({'employee_id': employees.employee_id, 'message': 'success'}), 200
            return jsonify({'message': 'you are not admin'}), 401
        except:
            return jsonify({'message': 'error'}), 404

    @token_required
    @swag_from("../swagger/swagger_get_emplist.yml")
    def get_emplist():
        try:
            token = request.headers['x-access-token']
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            lower = request.args.get('lower')
            upper = request.args.get('upper')
            search = request.args.get('search')
            if data['employee_role'] == "hr":
                employees = Employee.getlistemp(lower, upper, search)
                emplist = []
                for item in employees:
                    country = Country.lookup(item.country_id)
                    emplist.append({
                        'employee_id': item.employee_id,
                        'country_name': country.country_name,
                        'first_name': item.first_name,
                        'last_name': item.last_name,
                        'employee_code': item.employee_code,
                        'employee_role': item.employee_role
                        })
                return jsonify(emplist), 200
            return jsonify({'message': 'you are not admin'}), 400
        except:
            return jsonify({'message': 'error'}), 404

    @token_required
    @swag_from("../swagger/swagger_get_employee_by_id.yml")
    def get_empbyID(employee_id):
        try:
            emp = Employee.getempbyID(employee_id)
            if emp:
                countries = Country.lookup(emp.country_id)
                empdetails = ({
                    'employee_id': emp.employee_id,
                    'first_name': emp.first_name,
                    'country_name': countries.country_name,
                    'last_name': emp.last_name,
                    'employee_code': emp.employee_code,
                    'phno': emp.phno,
                    'email': emp.email,
                    'employee_role': emp.employee_role,
                    'gender': emp.gender,
                    'message': 'ok'
                    })
                return jsonify(empdetails)
            else:
                return jsonify({'message': 'emp not found'}), 400
        except:
            return jsonify({'message': 'error'}), 404

    @swag_from("../swagger/swagger_forgetpass_otp.yml")
    def forgetpass_otp():
        try:
            auth = request.form.get('auth')
            if re.match(r'[^@]+@[^@]+\.[^@]', auth):
                emp = Employee.query.filter_by(email=auth).first()
            elif re.match(r'["0-9"]{10}', auth):
                emp = Employee.query.filter_by(phone=auth).first()
            else:
                emp = Employee.query.filter_by(employee_code=auth).first()
            if emp:
                email = emp.email
                otp = SendOtp(email)
                Employee.addotp(emp.employee_id, otp)
                return jsonify({'employee_id': emp.employee_id, 'message': 'success'}), 200
            return jsonify({'message': 'wrong emp code or phno or email'}), 401
        except:
            return jsonify({'message': 'error'}), 404

    @swag_from("../swagger/swagger_changepass.yml")
    def changepass(employee_id):
        try:
            emp = Employee.getempbyID(employee_id)
            if emp:
                otp = request.form.get('otp')
                password = request.form.get('password')
                password2 = request.form.get('password2')
                if emp.otp != otp:
                    return jsonify({'message': 'wrong otp'}), 400
                if password != password2:
                    return jsonify({'message': 'password not match'}), 401
                Employee.updatepass(employee_id, hashlib.md5(password.encode()).hexdigest())
                return jsonify({'message': 'success'}), 200
            return jsonify({'message': 'error'}), 400
        except:
            return jsonify({'message': 'error'}), 404

    @token_required
    @swag_from("../swagger/swagger_update_emp.yml")
    def update_emp():
        try:
            token = request.headers['x-access-token']
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            emp = Employee.getempbyID(data['employee_id'])
            if emp:
                country_name = request.form.get('country_name')
                first_name = request.form.get('first_name')
                last_name = request.form.get('last_name')
                employee_role = request.form.get('employee_role')
                email = request.form.get('email')
                phno = request.form.get('phno')
                gender = request.form.get('gender')
                country_id = None
                if country_name != None:
                    country = Country.lookupbycname(country_name)
                    country_id = country.country_id
                employeelst = Employee.getempforupdate(data['employee_id'])
                emp_phlist = []
                emp_emaillist = []
                for item in employeelst:
                    emp_phlist.append(item.phno)
                    emp_emaillist.append(item.email)
                if phno in emp_phlist:
                    return jsonify({'message': 'ph no existes'}), 400
                if email in emp_emaillist:
                    return jsonify({'message': 'email no existes'}), 400
                emp = Employee.updateemp(data['employee_id'], country_id,
                                         first_name, last_name, employee_role, email, phno, gender)
                return jsonify({'message': 'success'}), 200
            return jsonify({'message': 'error'}), 404
        except:
            return jsonify({'message': 'error'}), 404

    @token_required
    @swag_from("../swagger/swagger_update_employee_by_id.yml")
    def update_empbyID(employee_id):
        try:
            token = request.headers['x-access-token']
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            if data['employee_role'] == "hr":
                emp = Employee.getempbyID(employee_id)
                if emp:
                    employee_code = request.form.get('employee_code')
                    country_name = request.form.get('country_name')
                    first_name = request.form.get('first_name')
                    last_name = request.form.get('last_name')
                    employee_role = request.form.get('employee_role')
                    email = request.form.get('email')
                    phno = request.form.get('phno')
                    gender = request.form.get('gender')
                    country_id = None
                    if country_name != None:
                        country = Country.lookupbycname(country_name)
                        country_id = country.country_id
                    employeelst = Employee.getempforupdate(employee_id)
                    emp_codelst = []
                    emp_phlist = []
                    emp_emaillist = []
                    for item in employeelst:
                        emp_codelst.append(item.employee_code)
                        emp_phlist.append(item.phno)
                        emp_emaillist.append(item.email)
                    if employee_code in emp_codelst:
                        return jsonify({'message': 'emp_code exists'}), 400
                    if phno in emp_phlist:
                        return jsonify({'message': 'ph no existes'}), 400
                    if email in emp_emaillist:
                        return jsonify({'message': 'email no existes'}), 400
                    emp = Employee.updateempHr(employee_id, employee_code, country_id, first_name,
                                               last_name, employee_role, email, phno, gender)
                    return jsonify({'message': 'success'}), 200
                return jsonify({'message': 'error'}), 400
            return jsonify({'message': 'you are not admin'}), 400
        except:
            return jsonify({'message': 'error'}), 404

    @token_required
    @swag_from("../swagger/swagger_delete_emp.yml")
    def delete_employee(employee_id):
        try:
            token = request.headers['x-access-token']
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            if data['employee_role'] == "hr":
                emp = Employee.getempbyID(employee_id)
                if emp:
                    Employee.delete(emp)
                    return jsonify({'message': 'success'}), 200
            return jsonify({'message': 'employee not found'}), 400
        except:
            return jsonify({'message': 'error'}), 404

    @swag_from("../swagger/swagger_login_employee.yml")
    # @cross_origin()
    def login_Emp():
        try:
            if request.method == 'POST':
                auth = request.form
                if not auth or not auth.get('employee_code') or not auth.get('password'):
                    return make_response(
                        'Could not verify', 401, {'WWW-Authenticate': 'Basic realm ="Login required !!"'})
                emp = Employee.query.filter_by(employee_code=auth.get('employee_code')).first()
                if not emp:
                    return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm ="User does not exist !!"'})
                password = auth.get('password')
                password = hashlib.md5(password.encode()).hexdigest()
                if password == emp.password:
                    token = jwt.encode({'employee_id': str(emp.employee_id),
                                        'employee_role': emp.employee_role,
                                        'exp': datetime.utcnow() + timedelta(minutes=TIME_JWT)},
                                       SECRET_KEY, algorithm="HS256")
                    return make_response(jsonify({'token': token,
                                                  'employee_id': emp.employee_id,
                                                  'employee_role': emp.employee_role}), 201)
                return make_response('could not veryfy!', 401, {'WWW-Authenticate': 'Basic realm ="Login required !!"'})
        except:
            return jsonify({'message': 'error'}), 404
