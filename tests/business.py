"""Test case for the user"""
import json
import datetime
from flask_jwt_extended import create_access_token
from tests.test_base import BaseTestCase


class TestPostBusiness(BaseTestCase):
    """Test for post business endpoint"""
    def test_business_creation(self):
        """Test user registration works correcty"""
        result = self.register_business()
        self.assertEqual(result['message'], "Business created successfully")

    def test_create_empty_field(self):
        """Test business creation with an empty description"""
        result = self.register_business(name="KTDA", description=" ",
                          category="Farming", location="Narok")
        self.assertEqual(result['message'], ['Please enter your description'])
    
    def test_json_request(self):
        """Test business creation with absent content type header"""
        self.register_user()
        login_res = self.login_user()
        result = json.loads(login_res.data.decode())
        change_res = self.client.post(
            '/api/v1/business',
            headers={'Authorization': 'Bearer ' + result['access_token']},
            data={})
        result = json.loads(change_res.data.decode())
        self.assertEqual(result['message'], "Bad Request. Request should be JSON format")
        self.assertEqual(change_res.status_code, 405)

    def test_missing_user(self):
        """Test business for unregistered user"""
        with self.app.app_context():
            business_data = {'name':'KTDA', 'description':'This is good', 'category':'Farming', 'location':'Narok'}
            access_token = create_access_token(identity=2, expires_delta=datetime.timedelta(hours=1))
            self.header['Authorization'] = 'Bearer ' + access_token
            res = self.make_request('/api/v1/business', data=business_data)
            result = json.loads(res.data.decode())
            self.assertEqual(result['message'], "Please login to continue")


class TestPutBusiness(BaseTestCase):
    """Test for editing business endpoint"""
    def test_business_can_be_edited(self):
        """Test API can edit an existing business"""
        business_data = {'name':'ABCD', 'description':'This is updated', 'category':'Farming', 'location':'Narok'}
        self.register_business()
        res = self.make_request('/api/v1/business/1', data=business_data, method='put')
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'], "Business updated successfully")

    def test_json_request(self):
        """Test edit business with absent content type header"""
        self.register_user()
        login_res = self.login_user()
        result = json.loads(login_res.data.decode())
        change_res = self.client.put(
            '/api/v1/business/1',
            headers={'Authorization': 'Bearer ' + result['access_token']},
            data={})
        result = json.loads(change_res.data.decode())
        self.assertEqual(result['message'], "Bad Request. Request should be JSON format")
        self.assertEqual(change_res.status_code, 405)

    def test_edit_empty_field(self):
        """Test business edit with an empty description"""
        business_data = {'name':'ABCD', 'category':'Farming', 'location':'Narok'}
        self.register_business()
        res = self.make_request('/api/v1/business/1', data=business_data, method='put')
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'], ['Please enter your description'])

    def test_non_existing_business(self):
        """Test editing non existing business"""
        business_data = {'name':'ABCD', 'description':'This is updated', 'category':'Farming', 'location':'Narok'}
        self.get_login_token()
        res = self.make_request('/api/v1/business/1', data=business_data, method='put')
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'], 'The operation is Forbidden')


class TestDeleteBusiness(BaseTestCase):
    """Test for delete business endpoint"""
    def test_business_can_be_deleted(self):
        """Test API can delete an existing business"""
        self.register_business()
        res = self.make_request('/api/v1/business/1', data={'password':'test1234'}, method='delete')
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'], 'Business deleted successfully')
    
    def test_delete_non_existing(self):
        """Test deleting a non existent business"""
        self.register_business()
        res = self.make_request('/api/v1/business/2', data={'password':'test1234'}, method='delete')
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'], 'The operation is Forbidden')
    
    def test_delete_invalid_password(self):
        """Test user provides a wrong password"""
        self.register_business()
        res = self.make_request('/api/v1/business/2', data={'password':'test123'}, method='delete')
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'], 'Invalid password')
    
    def test_delete_missing_password(self):
        """Test deleting with missing password"""
        self.register_business()
        res = self.make_request('/api/v1/business/2', data={}, method='delete')
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'],  ['Please enter your password'])

    def test_json_request(self):
        """Test deleting business with absent content type header"""
        self.register_user()
        login_res = self.login_user()
        result = json.loads(login_res.data.decode())
        change_res = self.client.delete(
            '/api/v1/business/1',
            headers={'Authorization': 'Bearer ' + result['access_token']},
            data={})
        result = json.loads(change_res.data.decode())
        self.assertEqual(result['message'], "Bad Request. Request should be JSON format")
        self.assertEqual(change_res.status_code, 405)


class TestGetBusiness(BaseTestCase):
    """Test for get business endpoint"""
    def test_get_all_businesses(self):
        """Test get paginated business list"""
        self.register_business()
        self.register_business()
        res = self.client.get('/api/v1/business')
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'], "The following business are available")
        self.assertEqual(result['next_page'], 2)

    def test_get_empty_business(self):
        """Test get empty business in database"""
        res = self.client.get('/api/v1/business')
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'], "There are no businesses registered currently")

    def test_get_business_by_id(self):
        """Test get business by id"""
        self.register_business()
        res = self.client.get('/api/v1/business/1')
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'], "Business found")

    def test_get_business_not_available(self):
        """Test get not available business by id"""
        res = self.client.get('/api/v1/business/1')
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'], "Resource not found")