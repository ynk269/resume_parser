from flask import request
from flask_restx import Api, Resource

from werkzeug.datastructures import FileStorage

from .service.file_handling import *

api = Api()

upload_parser = api.parser()
upload_parser.add_argument('file', location='files', type=FileStorage, required=True)


ALLOWED_EXTENSIONS = set(['pdf', 'png', 'jpg', 'jpeg', 'docx', 'doc'])

allowed_ext = ALLOWED_EXTENSIONS

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in allowed_ext

def init_routes(app):
    @api.route('/upload')
    class Upload(Resource):
        @api.expect(upload_parser)
        def post(self):
            file = request.files['file']
            if file and allowed_file(file.filename):
                handle_uploaded_file(file, app)
                dictionary = handle_file(file, app)
                return {'data': dictionary}, 200
            else:
                return {'message': 'File uploading failed'}, 403













# from flask import Flask, request
# from flask_restx import Api, Resource

# # from flask_sqlalchemy import SQLAlchemy
# from werkzeug.datastructures import FileStorage

# from .service.file_handling import *

# api = Api()

# upload_parser = api.parser()
# upload_parser.add_argument('file', location='files', type=FileStorage, required=True)


# ALLOWED_EXTENSIONS = set(['pdf', 'png', 'jpg', 'jpeg', 'docx', 'doc'])

# allowed_ext = ALLOWED_EXTENSIONS

# def allowed_file(filename):
#     return '.' in filename and \
#            filename.rsplit('.', 1)[1] in allowed_ext
 
# @api.route('/upload')
# class Upload(Resource):
#     @api.expect(upload_parser)
#     def post(self):
#         file = request.files['file']
#         if file and allowed_file(file.filename):
#             handle_uploaded_file(request.files['file'])
#             dictionary = handle_file(request.files['file'])
#             return {'data': dictionary}, 200
#         else:
#             return {'message': 'File uploading failed'}, 403