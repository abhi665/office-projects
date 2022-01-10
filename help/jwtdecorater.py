from flask import jsonify,request
import jwt
from functools import wraps
from models.employee import Employee
from flask_cors import cross_origin
SECRET_KEY = "SECRATE"


def token_required(f):
    @cross_origin()
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers['x-access-token']
        if not token:
            return jsonify({'message':'tokrn not found'}),403
        try:
            data = jwt.decode(token,SECRET_KEY,algorithms=["HS256"])
            emp = Employee.query.filter_by(employee_id = data['employee_id']).first()
        except:
            return jsonify({'message': 'token is missing or invalid'}),403
        return f(*args, **kwargs)
    return decorated