from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, World!'

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