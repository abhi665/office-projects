from flask import Flask
from flask_migrate import Migrate
from views.employee import Employeeview
from models.db import Database
from views.leave import Leave
from flasgger import Swagger
from flask_cors import CORS
app = Flask(__name__)

cors = CORS(app, resources={r"/*": {"origins": "*"}})

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


PREFIX = "/employee"

app.add_url_rule(PREFIX+"/", "create_employee", Employeeview.create_emp, methods=["POST"])

# app.add_url_rule(PREFIX+"/<lower>/<upper>", "list_employee/<lower>/<upper>", Employeeview.get_emplist, methods=["GET"])

app.add_url_rule(PREFIX+"/", "list_employee",Employeeview.get_emplist, methods=["GET"])

app.add_url_rule(PREFIX+"/<employee_id>", "list_employee/<employee_id>", Employeeview.get_empbyID, methods=["GET"])

app.add_url_rule(PREFIX+"/", "update_employee", Employeeview.update_emp, methods=["PUT"])

app.add_url_rule(PREFIX+"/<employee_id>", "update_employee/<employee_id>", Employeeview.update_empbyID, methods=["PUT"])

app.add_url_rule(PREFIX+"/<employee_id>", "delete_employee/<employee_id>", Employeeview.delete_employee, methods=["DELETE"])

app.add_url_rule(PREFIX+"/login", "login_Emp", Employeeview.login_Emp, methods=["POST"])

app.add_url_rule(PREFIX+"/forgetpassotp", "forgetpass_otp", Employeeview.forgetpass_otp, methods=["POST"])

app.add_url_rule(PREFIX+"/changepass/<employee_id>", "change_pass/<employee_id>", Employeeview.changepass, methods=["POST"])

app.add_url_rule('/leave/span',"span",Leave.leave_span,methods=["POST"])

app.add_url_rule('/leave/type',"type",Leave.leave_type,methods=["POST"])

# app.add_url_rule('/leave/allotment/<employee_id>',"allotment/<employee_id>",Leave.leave_allotment,methods=["POST"])

app.add_url_rule('/leave/allotment_reset',"allotment_reset",Leave.leave_allotment_reset,methods=["GET"])

app.add_url_rule('/leave/application',"application",Leave.leave_application,methods=["POST"])

app.add_url_rule('/leave/approvement',"approvement",Leave.Leave_approvement,methods=["POST"])

app.add_url_rule('/leave/get_leavelist',"get_leavelist",Leave.get_leavelist,methods=["GET"])

app.add_url_rule('/leave/get_listallotement',"get_listallotement",Leave.get_listallotement,methods=["GET"])

app.add_url_rule('/leave/addleave_allotment',"addleave_allotment",Leave.addleave_allotment,methods=["POST"])

app.add_url_rule('/leave/deleteLeavespan/<leave_span_id>',"Leavespan_delete",Leave.delete_leavespan,methods=["DELETE"])

app.add_url_rule('/leave/deleteLeavetype/<leave_type_id>',"Leavetype_delete",Leave.delete_leavetype,methods=["DELETE"])

app.add_url_rule('/leave/deleteLeaveallot/<employee_id>',"delete_leaveallotment",Leave.delete_leaveallotment,methods=["DELETE"])

if __name__ == '__main__':
    app.run(debug=True)
