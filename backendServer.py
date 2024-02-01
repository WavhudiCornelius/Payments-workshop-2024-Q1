from flask import Flask, jsonify
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

    field = request.args.get('field')
    error = request.args.get('error')


    cursor.execute(f'''
        SELECT *
        FROM error_info
        WHERE error_type = {error} AND field_type = {field} 
    ''')
    
    rows = cursor.fetchall()


    filtered_data = [
        {'id': row[0], 'date': row[1], 'field': row[2], 'error': error}
        for row in rows
    ]

    return jsonify(filtered_data)


if __name__ == '__main__':
    app.run(debug=True)