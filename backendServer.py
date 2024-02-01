from flask import Flask, jsonify, request
from payhealth_database import PayHealthDatabase
from payhealth_api_validate import payhealth_api_validate

app = Flask(__name__)


# Register the Blueprint
app.register_blueprint(payhealth_api_validate)


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



if __name__ == '__main__':
    app.run(debug=True)