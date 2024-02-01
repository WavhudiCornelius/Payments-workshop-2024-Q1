from flask import Flask
from payhealth_api_validate import payhealth_api_validate

app = Flask(__name__)

# Register the Blueprint
app.register_blueprint(payhealth_api_validate)

@app.route('/')
def hello():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(debug=True)