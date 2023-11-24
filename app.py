from flask import Flask
from controller.controller import form
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

# Register the Blueprint
app.register_blueprint(form, url_prefix='/api')
@app.route("/")
def trail():
    return "second12"



if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True,port=8001)
