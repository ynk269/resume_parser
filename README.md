.PHONY: clean system-packages python-packages install tests run all

system-packages:
   sudo apt install python-pip -y

prerequisites:
- Python 3.10 or higher
- Flask
- Flask-RESTX
- ntlk
- spacy
- pdfminer.six


python-packages:
   pip install -r requirements.txt


install: system-packages python-packages

API Endpoints:
- `POST /upload`
- Description: Upload a file and process it.
- Request Body: FormData with a file field named 'file'.
- Response: JSON containing processed data.

run:
   flask run