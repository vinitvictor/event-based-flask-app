# event-based-flask-app
## Problem statement  
Use an event-driven architecture to read a text file and store it in a document database. The user should be able to see the data on the front end, and upon the request from the user, the saved data will be converted to CSV and delivered to the user as a downloadable URL.

## Environment 
  - Python Flask framework to build the web app.
  - Serverless framework to deploy the project.
  - Swagger for API documentation


## AWS Services  

### S3 Buckets 
  - Input Bucket (Files will be dropeed here)
  - Output Bucket (converted CSV files will be stored here)

### Lambda  
  - Text to dynamodb table 
    - I've created a trigger from S3 input bucket to invoke this lambda. This lambda will read the text file and save it in dynamodb table.
    - The logic to transfer text data to dynamodb table and converting data in document format will be hold by this lambda.
    
  - Convert to csv
    - On demand this lambda will be invoked. It will fetch file from dynamodb and convert it to csv. 
    After conversion store that file to output bucket and share URL with user on front end.
  
### Dynamodb Schema  
  - Table Name - file_and_content
  - Schema 
    - file_name -> String
    - content -> Object (converted to store it in document format (key - Value pair))
    - raw_data -> raw-data 
    
## API Documentation

### Swagger 
  - Used swagger to build the api documentation. ( once you deploy the flask app, use '/apidocs' route to access the swagger documentation )
  - Created following APIs
    - Get - /download/{key}
      - To get the url of converted csv file
    - Get - /get-item/{key}
      - Get stored file in dynamodb and show it in tabular format to user
    - Get - /get-raw-data/{key}
      - Get stored file in dynamodb and show the raw data in a block
    - Post - /upload (additional to add new files to ddb)
      - Drop files in s3 input bucket

    

## Local Setup 

Please do the inital setup for serverless - https://www.serverless.com/framework/docs/getting-started

  1. Clone the project
  2. Create virtual environments 
  
   ```	
    $ virtualenv venv --python=python3
    $ source venv/bin/activate
  ```
  3. If any dependency is missing install it with 
  

    $ pip install <missing dependency>
    
  4. use following command to start server locally 
  
    $ sls wsgi server
    
  5. go to localhost:5000 - The flask application will be running.
  
  
## Server Deployment
   1. Once you have set up serverless dashboard and aws credentials in provider section. You can deploy this project using serveless.
   2. Follow same procedure from local setup till 4.
   3. use following command to deploy
    
     $ sls deploy
   
  Note - Server deployed links are attached in mail.
    

    
