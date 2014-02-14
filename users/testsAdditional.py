import unittest
import os
import httplib
import json

SERVER = "enigmatic-dusk-1170.herokuapp.com"

class TestLogin(unittest.TestCase):
    """Test proper handling of logging in."""

    SUCCESS =              1     #: a success
    ERR_BAD_CREDENTIALS = -1     #: (for login only) cannot find the user/password pair in the database

    def setUp(self):
        """Create the connection."""
        self.conn = httplib.HTTPConnection(SERVER, timeout=5)
        self.makeRequest("/TESTAPI/resetFixture")

    def tearDown(self):
        """Close the conection"""
        self.conn.close()

    def makeRequest(self, url, data = {}):
        """Issues a POST request containing DATA to the specified URL.
        This code is adapted from the same method in testLib.py"""
        headers = {}
        body = ''
        if data:
            headers = {"content-type": "application/json"}
            body = json.dumps(data)
        try:
            self.conn.request("POST", url, body, headers)
            self.conn.sock.settimeout(100.0) # Give time to the remote server to start and respond
            resp = self.conn.getresponse()
            data_string = "<unknown"
        
            if resp.status == 200:
                data_string = resp.read()
                response = json.loads(data_string)
                return response
            else:
                self.assertEquals(200, resp.status)
        except:
            raise

    def assertResponse(self, respData, count = None, errCode = SUCCESS):
        """
        Check that the response data dictionary matches the expected values
        """
        #from testLib.py
        expected = { 'errCode' : errCode }
        if count is not None:
            expected['count']  = count
        self.assertDictEqual(expected, respData)
    
    def testProper(self):
        """Test that the API properly handles correct behavior."""
        user1 = {'user': 'test1', 'password': 'swordfish'}
        self.makeRequest("/users/add", data = user1)
        response = self.makeRequest("/users/login", data = user1)
        self.assertResponse(response, count=2)

    def testBadCreds(self):
        """Test that the API properly handles incorrect behavior."""
        user2 = {'user': 'test2', 'password': ''}
        self.makeRequest("/users/add", data = user2)
        response = self.makeRequest("/users/login", data = {'user': 'test2', 'password': 'pass'})
        self.assertResponse(response, errCode = self.ERR_BAD_CREDENTIALS)
        response = self.makeRequest("/users/login", data = {'user': 'test3', 'password': ''})
        self.assertResponse(response, errCode = self.ERR_BAD_CREDENTIALS)

class TestResetFixture(unittest.TestCase):
    """Test the resetFixture behavior."""

    SUCCESS =              1     #: a success
    ERR_BAD_CREDENTIALS = -1     #: (for login only) cannot find the user/password pair in the database
    ERR_USER_EXISTS     = -2     #: (for add only) trying to add a user that already exists
    ERR_BAD_USERNAME    = -3     #: (for add, or login) invalid user name (only empty string is invalid for now)
    ERR_BAD_PASSWORD    = -4

    def setUp(self):
        """Create the connection."""
        self.conn = httplib.HTTPConnection(SERVER, timeout=5)
        self.makeRequest("/TESTAPI/resetFixture")

    def tearDown(self):
        """Close the conection"""
        self.conn.close()

    def makeRequest(self, url, data = {}):
        """Issues a POST request containing DATA to the specified URL.
        This code is adapted from the same method in testLib.py"""
        headers = {}
        body = ''
        if data:
            headers = {"content-type": "application/json"}
            body = json.dumps(data)
        try:
            self.conn.request("POST", url, body, headers)
            self.conn.sock.settimeout(100.0) # Give time to the remote server to start and respond
            resp = self.conn.getresponse()
            data_string = "<unknown"
        
            if resp.status == 200:
                data_string = resp.read()
                response = json.loads(data_string)
                return response
            else:
                self.assertEquals(200, resp.status)
        except:
            raise
    
    def assertResponse(self, respData, count = None, errCode = SUCCESS):
        """
        Check that the response data dictionary matches the expected values
        """
        #from testLib.py
        expected = { 'errCode' : errCode }
        if count is not None:
            expected['count']  = count
        self.assertDictEqual(expected, respData)
        
    def testResest(self):
        """Test the resetFixture API capability."""
        data = {'user': 'test3', 'password': 'pass1'}
        self.makeRequest("/users/add", data = data)
        self.makeRequest("/users/login", data = data)
        response = self.makeRequest("/users/login", data = data)
        self.assertResponse(response, count=3)
        response = self.makeRequest("/TESTAPI/resetFixture", data = {})
        self.assertResponse(response)
        response = self.makeRequest("/users/login", data = data)
        self.assertResponse(response, errCode=self.ERR_BAD_CREDENTIALS)     #test3 doesn't exist anymore
        response = self.makeRequest("/users/add", data = data)
        self.assertResponse(response, count=1)                              #but it can be added

    def testComprehensive(self):
        """Put it all together now."""
        user1 = {'user': 'user', 'password': ''}
        response = self.makeRequest("/users/add", data = user1)          #Doesn't exist, so it can be created (even without a password)
        self.assertResponse(response, count=1)
        response = self.makeRequest("/users/add", data = user1)          #But it can't be created again
        self.assertResponse(response, errCode=self.ERR_USER_EXISTS)
        user2 = {'user': 'test', 'password': '123456'}
        response = self.makeRequest("/users/add", data = user2)          #A second user can be created though
        self.assertResponse(response, count=1)
        response = self.makeRequest("/users/login", data = user2)        #And if the credentials match, you can log in
        self.assertResponse(response, count=2)
        user3 = {'user': '', 'password': ''}
        response = self.makeRequest("/users/add", data = user3)          #But you have to have a username
        self.assertResponse(response, errCode=self.ERR_BAD_USERNAME)
        user4 = {'user': 'John Q. Public', 'password': 'Sons of Liberty'}
        response = self.makeRequest("/users/login", data = user4)        #And you have to exist before you can log in
        self.assertResponse(response, errCode=self.ERR_BAD_CREDENTIALS)
        response = self.makeRequest("/TESTAPI/resetFixture", data = {})  #And now the database is empty again
        self.assertResponse(response)
        response = self.makeRequest("/users/login", data = user2)        #Since the database is empty, we can't log in any more
        self.assertResponse(response, errCode=self.ERR_BAD_CREDENTIALS)
        response = self.makeRequest("/users/add", data = user4)          #But we can still add new users
        self.assertResponse(response, count=1)
        response = self.makeRequest("/users/login", data = user4)        #And this time, we can log in
        self.assertResponse(response, count=2)
        response = self.makeRequest("/users/add", data = user2)          #Nothing stopping us from recreating the user
        self.assertResponse(response, count=1)
        response = self.makeRequest("/users/login", data = user2)        #Now we can log in again
        self.assertResponse(response, count=2)
        
        

        
class TestAddUser(unittest.TestCase):
    """Test adding users"""

    SUCCESS =              1     #: a success
    ERR_USER_EXISTS     = -2     #: (for add only) trying to add a user that already exists
    ERR_BAD_USERNAME    = -3     #: (for add, or login) invalid user name (only empty string is invalid for now)
    ERR_BAD_PASSWORD    = -4

    def setUp(self):
        """Create the connection."""
        self.conn = httplib.HTTPConnection(SERVER, timeout=5)
        self.makeRequest("/TESTAPI/resetFixture")

    def tearDown(self):
        """Close the conection"""
        self.conn.close()

    def makeRequest(self, url, data = {}):
        """Issues a POST request containing DATA to the specified URL.
        This code is adapted from the same method in testLib.py"""
        headers = {}
        body = ''
        if data:
            headers = {"content-type": "application/json"}
            body = json.dumps(data)
        try:
            self.conn.request("POST", url, body, headers)
            self.conn.sock.settimeout(100.0) # Give time to the remote server to start and respond
            resp = self.conn.getresponse()
            data_string = "<unknown"
        
            if resp.status == 200:
                data_string = resp.read()
                response = json.loads(data_string)
                return response
            else:
                self.assertEquals(200, resp.status)
        except:
            raise
    
    def assertResponse(self, respData, count = 1, errCode = SUCCESS):
        """
        Check that the response data dictionary matches the expected values
        """
        #from testLib.py
        expected = { 'errCode' : errCode }
        if count is not None:
            expected['count']  = count
        self.assertDictEqual(expected, respData)

    def testAdd(self):
        """Simple user adding test"""
        response = self.makeRequest("/users/add", data = {'user': 'user', 'password': 'password'})
        self.assertResponse(response)

    def testDupeAdd(self):
        """Shouldn't be able to add the same user twice."""
        self.makeRequest("/users/add", data = {'user' : 'user1', 'password' : 'password'})
        response = self.makeRequest("/users/add", data = {'user' : 'user1', 'password' : 'password'})
        self.assertResponse(response, count=None, errCode = self.ERR_USER_EXISTS)

    def testLong(self):
        """ Test length checking."""
        longstring = 129 * '*'
        response = self.makeRequest("/users/add", data = {'user' : longstring, 'password' : 'password'})
        self.assertResponse(response, count=None, errCode = self.ERR_BAD_USERNAME)
        response = self.makeRequest("/users/add", data = {'user' : 'user', 'password' : longstring})
        self.assertResponse(response, count=None, errCode = self.ERR_BAD_PASSWORD)

    
