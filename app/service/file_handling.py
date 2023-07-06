import os
import io
import filetype

from pdfminer.layout import LAParams, LTTextBox
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator, TextConverter


from .makeform import *
from .demo import *



ALLOWED_EXTENSIONS = set(['pdf', 'png', 'jpg', 'jpeg', 'docx', 'doc'])

allowed_ext = ALLOWED_EXTENSIONS

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in allowed_ext


def handle_uploaded_file(f, app):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], f.filename)
    f.save(file_path)


def handle_file(file, app):
    """
    Find the file filetype
    Handle the file path and find the extension of the file path
    and convert pdf and extract the text from the pdf

    Args:
        file (FileStorage): Uploaded file
        app (Flask): Flask application object
    """
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    
    kind = filetype.guess(file_path)
    if kind is None:
        print('Cannot guess file type!')
        return {}
        
    print('File extension: ', kind.extension)
    print('File MIME type: ', kind.mime)

    if kind.extension == "pdf":
        resource_manager = PDFResourceManager()
        fake_file_handle = io.StringIO()
        codec = 'utf-8'
        converter = TextConverter(resource_manager, fake_file_handle, codec=codec, laparams=LAParams())
        page_interpreter = PDFPageInterpreter(resource_manager, converter)
        
        with open(file_path, 'rb') as fh:
            for page in PDFPage.get_pages(fh, caching=True, check_extractable=True):
                page_interpreter.process_page(page)
                text = fake_file_handle.getvalue()
                
        converter.close()
        fake_file_handle.close()

        dictionary = MakeForm(text)

        pymudf_parser(file_path)

        return dictionary

    return {}


# def handle_file(filepath, app):
#     """
#     Find the file filetype
#     Handle the filepath and find the extension of the file path
#     and conevert pdf and ext6ract the text from the pdf

#     Args:
#         filepath (_type_): _description_
#     """
    
#     kind = filetype.guess(filepath)
#     if kind is None:
#         print('Cannot guess file type!')
        
#     print('File extension: ', kind.extension)
#     print('File MIME type: ', kind.mime)
# 	# print('File MIME type: ', kind.mime)
 
#     if(kind.extension=="pdf"):
#         resource_manager = PDFResourceManager()
#         # print(resource_manager)
#         fake_file_handle = io.StringIO()
#         # print(fake_file_handle, 'fake handler')
#         codec='utf-8'
#         converter = TextConverter(resource_manager, fake_file_handle,codec=codec, laparams=LAParams())
#         # print('converter-----', converter)
#         page_interpreter = PDFPageInterpreter(resource_manager, converter)
#         # print(page_interpreter, '---page_interpreter')
#         with open('app/static/upload/'+filepath.filename, 'rb') as fh:
#             for page in PDFPage.get_pages(fh,caching=True,check_extractable=True):
#                 page_interpreter.process_page(page)
#                 text = fake_file_handle.getvalue()
                
#         converter.close()
#         fake_file_handle.close()
#         # print('print the text \n',text)

#     dictionary=MakeForm(text)

#     pymudf_parser('app/static/upload/'+filepath.filename)

#     return dictionary