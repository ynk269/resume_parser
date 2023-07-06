from flask import Flask
from flask_cors import CORS

from .route import api, init_routes

def create_app():
    app = Flask(__name__)
    api.init_app(app)

    app.config['UPLOAD_FOLDER'] = 'app/static/upload/'

    cors_config_par = {
        "origins": [
            "http://localhost:4200",
        ],
        "methods": ["OPTIONS", "GET", "POST", "HEAD", "PUT", "PATCH", "DELETE"]
    }
    
    cors = CORS(app, resources={r"/*": cors_config_par})

    init_routes(app)  # Pass the app object to the init_routes function

    return app






# from flask import Flask
# from flask_cors import CORS

# from .route import api

# # from .routes import ns


# def create_app():
#     app = Flask(__name__)
#     api.init_app(app)

#     app.config['UPLOAD_FOLDER'] = 'app/static/uploads'

#     cors_config_par = {
#         "origins": [
#             "http://localhost:4200",
#         ],
#         "methods": ["OPTIONS", "GET", "POST", "HEAD", "PUT", "PATCH", "DELETE"]
#     }
    
#     cors = CORS(app, resources={r"/*": cors_config_par})

    

#     return app