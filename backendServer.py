from flask import Flask, jsonify, request
from payhealth_database import PayHealthDatabase
import json
import re
from validation_errors import ValidationError
from collections import OrderedDict
from payhealth_database import PayHealthDatabase

app = Flask(__name__)

database = PayHealthDatabase()

database.initialize_database()

@app.route('/test' , methods=['POST'])
def create_test_data():
    field = request.args.get('field')
    error = request.args.get('error')            
    try:
        database.save_error_info(field, error)
        return "yay"
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/payhealth/reporting', methods=['GET'])
def reporting_endpoint():
    try:
        field = request.args.get('field')        
        error_records = database.get_error_records_by_field_name(field)

        result = [
            {
                'id': record[0],
                'field_name': record[1],
                'error_type': record[2],
                'error_date': record[3]
            }
            for record in error_records
        ]

        return jsonify(result)

    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500


@app.route('/api/payhealth/', methods=['POST'])
def payhealth():
    data = request.json
    validation_results = []

    # Extract and validate data
    name = data.get("name", "")
    email = data.get("email", "")
    age = data.get("age", "0")

    # Initialize response dictionary as OrderedDict
    response = OrderedDict()

    # Validate Name
    if not all(char.isalpha() or char.isspace() for char in name):
        validation_results.append({"field": "name", "success": False, "error": ValidationError.ERR_NAME_ALPHA.name, "errorText": ValidationError.ERR_NAME_ALPHA.value})
    elif any(char in set('!@#$%^&*()[]{};:,./<>?\|`~-=_+') for char in name):
        validation_results.append({"field": "name", "success": False, "error": ValidationError.ERR_NAME_SPECIAL_CHAR.name, "errorText": ValidationError.ERR_NAME_SPECIAL_CHAR.value})
    else:
        validation_results.append({"field": "name", "success": True, "error": None, "errorText": None})

    # Validate Email
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        validation_results.append({"field": "email", "success": False, "error": ValidationError.ERR_EMAIL_INVALID.name, "errorText": ValidationError.ERR_EMAIL_INVALID.value})
    else:
        validation_results.append({"field": "email", "success": True, "error": None, "errorText": None})

    # Validate Age
    try:
        age = int(age)
        if age < 18:
            validation_results.append({"field": "age", "success": False, "error": "ERR_AGE_TOO_YOUNG", "errorText": "Age must not be younger than 18."})
        elif age > 150:
            validation_results.append({"field": "age", "success": False, "error": "ERR_AGE_TOO_OLD", "errorText": "Age must not be older than 150."})
        else:
            validation_results.append({"field": "age", "success": True, "error": None, "errorText": None})
    except ValueError:
        validation_results.append({"field": "age", "success": False, "error": "ERR_AGE_INVALID", "errorText": "Invalid age value."})

    # Insert error info into the database if there are errors
    for result in validation_results:
        if not result['success']:
            database.save_error_info(result['field'], result['error'])
            
    # Construct the response dictionary using OrderedDict
    response["name"] = name
    response["email"] = email
    response["age"] = age
    response["validation"] = validation_results

    # Serialize the response with sort_keys=False to maintain the order
    response_json = json.dumps(response, sort_keys=False)

    return response_json


if __name__ == '__main__':
    app.run(debug=True)