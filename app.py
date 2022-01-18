from flask import Flask
from flask_migrate import Migrate
from views.employee import Employeeview
from models.db import Database
from flasgger import Swagger
from flask_cors import  CORS
app = Flask(__name__)

cors = CORS(app,resources={r"/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'

db = Database.connect(app)

app.config["SWAGGER"] = {"tittle": "Swagger-UI", "universion": 2}

migrate = Migrate(app, db)



swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": "",
            "route": "/swag",
            # "rule_filter": lambda rule: True,
            # "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/swagger/",
}

swagger = Swagger(app, config=swagger_config)


# @app.after_request

# def after_request(response):
#   response.headers.add('Access-Control-Allow-Origin', '*')
#   response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
#   response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
#   return response


PREFIX = "/employee"

app.add_url_rule(PREFIX+"/", "create_employee", Employeeview.create_emp, methods=["POST"])

app.add_url_rule(PREFIX+"/<search>/<lower>/<upper>", "list_employee/<search>/<lower>/<upper>", Employeeview.get_emplist, methods=["GET"])

app.add_url_rule(PREFIX+"/<employee_id>", "list_employee/<employee_id>", Employeeview.get_empbyID, methods=["GET"])

app.add_url_rule(PREFIX+"/", "update_employee", Employeeview.update_emp, methods=["PUT"])

app.add_url_rule(PREFIX+"/<employee_id>", "update_employee/<employee_id>", Employeeview.update_empbyID, methods=["PUT"])

app.add_url_rule(PREFIX+"/<employee_id>", "delete_employee/<employee_id>", Employeeview.delete_employee, methods=["DELETE"])

app.add_url_rule(PREFIX+"/<search>/<lower>/<upper>", "list_employee/<search>/<lower>/<upper>", Employeeview.get_emplist, methods=["GET"])

app.add_url_rule(PREFIX+"/login", "login_Emp", Employeeview.login_Emp, methods=["POST"])

app.add_url_rule(PREFIX+"/forgetpassotp", "forgetpass_otp", Employeeview.forgetpass_otp, methods=["POST"])

app.add_url_rule(PREFIX+"/changepass/<employee_id>", "change_pass/<employee_id>", Employeeview.changepass, methods=["POST"])

if __name__ == '__main__':
    app.run(debug=True)
