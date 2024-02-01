# Import necessary modules
import json
from flask import Blueprint, request, jsonify
import re
from payhealth_database import PayHealthDatabase  # Import the PayHealthDatabase class
from validation_errors import ValidationError
from collections import OrderedDict

# Create a Blueprint
payhealth_api_validate = Blueprint('payhealth_api_validate', __name__)

# Initialize the PayHealthDatabase
db = PayHealthDatabase()

# Define the POST route
@payhealth_api_validate.route('/api/payhealth/', methods=['POST'])
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
        validation_results.append({"field": "age", "success": False, "error": ValidationError.ERR_AGE_UNDER.name, "errorText": ValidationError.ERR_AGE_UNDER.value})

    # Insert user data into the database and get user_id
    user_id = db.insert_user_info(name, age, email)

    # Insert error info into the database if there are errors
    for result in validation_results:
        if not result['success']:
            db.save_error_info(result['field'], result['error'])

    # Construct the response dictionary using OrderedDict
    response["name"] = name
    response["email"] = email
    response["age"] = age
    response["validation"] = validation_results

    # Serialize the response with sort_keys=False to maintain the order
    response_json = json.dumps(response, sort_keys=False)

    return response_json
