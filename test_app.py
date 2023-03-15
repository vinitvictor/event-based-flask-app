import unittest
import io
import json
from unittest.mock import patch, MagicMock

from app import app


class TestApp(unittest.TestCase):
    #app config
    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    #test for home page
    def test_main_page(self):
        response = self.app.get('/')
        self.assertIn(b'Uploaded Files', response.data)

    #test for upload feature
    def test_upload_file(self):
        with patch('aws_controller.upload_file', MagicMock(return_value={'status': 'success', 'message': 'File uploaded successfully'})):
            file_content = (io.BytesIO(b'Test data'), 'test.txt')
            response = self.app.post('/upload', data={'file': file_content})
            data = json.loads(response.data)
            self.assertEqual(data['status'], 'success')
            self.assertEqual(data['message'], 'File uploaded successfully')

    #checking get a file and show in tabular format
    def test_get_items(self):
        with patch('aws_controller.get_item', MagicMock(return_value={'Item':
        {
          "file_name": {
            "S": "test.txt"
          },
          "content": {
            "S": "[{\"id\": \"1\", \"first_name\": \"Beryle\", \"last_name\": \"Denzilow\", \"email\": \"bdenzilow0@buzzfeed.com\", \"gender\": \"Female\", \"ip_address\\r\": \"206.112.181.203\\r\"}]"
          },
          "raw_data": {
            "S": "id,first_name,last_name,email,gender,ip_address\r\n1,Beryle,Denzilow,bdenzilow0@buzzfeed.com,Female,206.112.181.203\r\n"
          }
        }})):
            response = self.app.get('/get-item/test.txt')
            self.assertIn(b'<title>test.txt</title>', response.data)

    #test case to get a file and show raw data
    def test_get_raw_data(self):
        with patch('aws_controller.get_item', MagicMock(return_value={'Item':
        {
          "file_name": {
            "S": "test.txt"
          },
          "content": {
            "S": "[{\"id\": \"1\", \"first_name\": \"Beryle\", \"last_name\": \"Denzilow\", \"email\": \"bdenzilow0@buzzfeed.com\", \"gender\": \"Female\", \"ip_address\\r\": \"206.112.181.203\\r\"}]"
          },
          "raw_data": {
            "S": "id,first_name,last_name,email,gender,ip_address\r\n1,Beryle,Denzilow,bdenzilow0@buzzfeed.com,Female,206.112.181.203\r\n"
          }
        }})):
            response = self.app.get('/get-raw-data/test.txt')
            self.assertIn(b'<title>test.txt Raw Data</title>', response.data)

    #test case to get the csv file
    def test_get_csv(self):
        with patch('aws_controller.get_file_url', MagicMock(return_value={'Payload': io.BytesIO(json.dumps({'statusCode': 200, 'body': {'url': 'http://example.com'}}).encode())})):
            response = self.app.get('/download/test.txt')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'http://example.com', response.data)

    def test_page_not_found(self):
        response = self.app.get('/does-not-exist')
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'404', response.data)

if __name__ == '__main__':
    unittest.main()
