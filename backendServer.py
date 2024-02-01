from flask import Flask, jsonify, request
from payhealth_database import PayHealthDatabase

app = Flask(__name__)

database = PayHealthDatabase()

database.initialize_database()

@app.route('/')
def hello():
    try:
        database.save_error_info("example_field", "example_error")
        records = database.get_error_records_by_field_name("example_field")
        return jsonify(records)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/payhealth/reporting', methods=['GET'])
def reporting_endpoint():
    try:

        field = request.args.get('field')
        error = request.args.get('error')


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