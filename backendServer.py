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

if __name__ == '__main__':
    app.run(debug=True)