from flask import Flask, jsonify, request
from api.routes.decision import decision_routes

def create_app():
    app = Flask(__name__)
    app.register_blueprint(decision_routes, url_prefix='/api')
    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
