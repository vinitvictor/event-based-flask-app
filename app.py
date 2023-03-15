from flask import Flask, jsonify,render_template,request
from flasgger import Swagger
from dynamodb_json import json_util as dbjson
import aws_controller
import json
import requests


app = Flask(__name__)

@app.before_first_request
def get_host():
    template = {
      "swagger": "2.0",
      "info": {
        "title": "Event based Application",
        "description": "Convert txt file to csv using event based architecture",
        "version": "0.0.1"
      },
      "host": "",
      "basePath": "/dev",  # change it to "/" when running locally
    }
    template['host'] = request.host
    # recreate the Swagger UI with the updated configuration
    global swagger
    swagger = Swagger(app,template=template)

#home page which will show all files in table
@app.route('/')
def main():
    result = dbjson.loads(aws_controller.get_fileNames())
    listConversion = list(result)
    values = listConversion
    return render_template("Index.html", rows=values)

#upload a file to s3
@app.route('/upload', methods=['POST'])
def upload_file():
    """
    Upload File to S3
    ---
    parameters:
      - name: file
        in: formData
        type: file
        required: true
        description: Upload a file.
    responses:
      200:
        description: return a row from dynamodb based on the file-name
    """


    fileStatus = aws_controller.upload_file(request)
    return fileStatus

#get single file details on-demand
@app.route('/get-item/<string:key>', methods=['GET'])
def get_items(key):
    """
    Get Item Page
    It returns the file in document format and converts it in tabular format to read
    ---
    parameters:
      - name: key
        in: path
        type: string
        required: true
        description: The file name.
    responses:
      200:
        description: return a row from dynamodb based on the file-name
    """
    try:
        result = json.loads(aws_controller.get_item(key)['Item']['content']['S'])
        header = result[0].keys()
        values = result
        return render_template("get-item.html",header = header,rows=values,file_name = key)
    except Exception as e:
        return render_template('400.html'), 400


#get single file details on-demand
@app.route('/get-raw-data/<string:key>', methods=['GET'])
def get_raw_data(key):
    """
    Raw Data Page
    It returns the file in document format and return the raw format it was uploaded
    ---
    parameters:
      - name: key
        in: path
        type: string
        required: true
        description: The file name.
    responses:
      200:
        description: return a row from dynamodb based on the file-name
    """
    try:
        result = aws_controller.get_item(key)['Item']['raw_data']['S']
        return render_template("raw-data.html",raw_data = result.split("\n"),file_name=key)
    except Exception as e:
        return render_template('400.html'), 400


#Download file on-demand
@app.route('/download/<string:key>', methods=['GET'])
def get_csv(key):
    """
    Output Link Page
    Invoke a lambda function to convert the file in csv and upload it to a
    differnt s3 bucket and return the url link
    ---
    parameters:
      - name: key
        in: path
        type: string
        required: true
        description: The file name.
    responses:
      200:
        description: return link for csv converted file
    """
    response = aws_controller.get_file_url(key)
    payload = json.loads(response['Payload'].read())
    if(payload['statusCode']==200):
        urlLink = payload['body']['url']
        return render_template("output-link.html",file_link = urlLink,file_name=key)
    else:
        return render_template('400.html'), 400

@app.errorhandler(404)
def page_not_found(error):
    """
    404 Page Not Found
    This endpoint returns a 404 error page.
    ---
    responses:
      404:
        description: 404 Page Not Found
    """
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)
