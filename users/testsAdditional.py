"""
Each file that starts with test... in this directory is scanned for subclasses of unittest.TestCase or testLib.RestTestCase
"""

import unittest
import os
import testLib

#Not my test, but left in to test unitTests
class TestUnit(testLib.RestTestCase):
    """Issue a REST API request to run the unit tests, and analyze the result"""
    def testUnit(self):
        respData = self.makeRequest("/TESTAPI/unitTests", method="POST")
        self.assertTrue('output' in respData)
        print ("Unit tests output:\n"+
               "\n***** ".join(respData['output'].split("\n")))
        self.assertTrue('totalTests' in respData)
        print "***** Reported "+str(respData['totalTests'])+" unit tests. nrFailed="+str(respData['nrFailed'])
        # When we test the actual project, we require at least 10 unit tests
        minimumTests = 10
        if "SAMPLE_APP" in os.environ:
            minimumTests = 4
        self.assertTrue(respData['totalTests'] >= minimumTests,
                        "at least "+str(minimumTests)+" unit tests. Found only "+str(respData['totalTests'])+". use SAMPLE_APP=1 if this is the sample app")
        self.assertEquals(0, respData['nrFailed'])

class TestLogin(testLib.RestTestCase):
    """Test proper handling of logging in."""
    def assertResponse(self, respData, count = None, errCode = testLib.RestTestCase.SUCCESS):
        """
        Check that the response data dictionary matches the expected values
        """
        expected = { 'errCode' : errCode }
        if count is not None:
            expected['count']  = count
        self.assertDictEqual(expected, respData)
    
    def testProper(self):
        """Test that the API properly handles correct behavior."""
        user1 = {'user': 'test1', 'password': 'swordfish'}
        self.makeRequest("/users/add", method="POST", data = user1)
        response = self.makeRequest("/users/login", method="POST", data = user1)
        self.assertResponse(response, count=2)

    def testBadCreds(self):
        """Test that the API properly handles incorrect behavior."""
        user2 = {'user': 'test2', 'password': ''}
        self.makeRequest("/users/add", method="POST", data = user2)
        response = self.makeRequest("/users/login", method="POST", data = {'user': 'test2', 'password': 'pass'})
        self.assertResponse(response, errCode = testLib.RestTestCase.ERR_BAD_CREDENTIALS)
        response = self.makeRequest("/users/login", method="POST", data = {'user': 'test3', 'password': ''})
        self.assertResponse(response, errCode = testLib.RestTestCase.ERR_BAD_CREDENTIALS)

class TestResetFixture(testLib.RestTestCase):
    """Test the resetFixture behavior."""
    def assertResponse(self, respData, count = None, errCode = testLib.RestTestCase.SUCCESS):
        """
        Check that the response data dictionary matches the expected values
        """
        expected = { 'errCode' : errCode }
        if count is not None:
            expected['count']  = count
        self.assertDictEqual(expected, respData)
        
    def testResest(self):
        data = {'user': 'test3', 'password': 'pass1'}
        self.makeRequest("/users/add", method="POST", data = data)
        self.makeRequest("/users/login", method="POST", data = data)
        response = self.makeRequest("/users/login", method="POST", data = data)
        self.assertResponse(response, count=3)
        response = self.makeRequest("/TESTAPI/resetFixture", method="POST", data = {})
        self.assertResponse(response)
        response = self.makeRequest("/users/login", method="POST", data = data)
        self.assertResponse(response, errCode = testLib.RestTestCase.ERR_BAD_CREDENTIALS) #test3 doesn't exist anymore
        response = self.makeRequest("/users/add", method="POST", data = data)
        self.assertResponse(response, count=1)                                            #but it can be added

    def testComprehensive(self):
        """Put it all together now."""
        user1 = {'user': 'user', 'password': ''}
        response = self.makeRequest("/users/add", method="POST", data = user1)          #Doesn't exist, so it can be created (even without a password)
        self.assertResponse(response, count=1)
        response = self.makeRequest("/users/add", method="POST", data = user1)          #But it can't be created again
        self.assertResponse(response, errCode=testLib.RestTestCase.ERR_USER_EXISTS)
        user2 = {'user': 'test', 'password': '123456'}
        response = self.makeRequest("/users/add", method="POST", data = user2)          #A second user can be created though
        self.assertResponse(response, count=1)
        response = self.makeRequest("/users/login", method="POST", data = user2)        #And if the credentials match, you can log in
        self.assertResponse(response, count=2)
        user3 = {'user': '', 'password': ''}
        response = self.makeRequest("/users/add", method="POST", data = user3)          #But you have to have a username
        self.assertResponse(response, errCode=testLib.RestTestCase.ERR_BAD_USERNAME)
        user4 = {'user': 'John Q. Public', 'password': 'Sons of Liberty'}
        response = self.makeRequest("/users/login", method="POST", data = user4)        #And you have to exist before you can log in
        self.assertResponse(response, errCode=testLib.RestTestCase.ERR_BAD_CREDENTIALS)
        response = self.makeRequest("/TESTAPI/resetFixture", method="POST", data = {})  #And now the database is empty again
        self.assertResponse(response)
        response = self.makeRequest("/users/login", method="POST", data = user2)        #Since the database is empty, we can't log in any more
        self.assertResponse(response, errCode=testLib.RestTestCase.ERR_BAD_CREDENTIALS)
        response = self.makeRequest("/users/add", method="POST", data = user4)          #But we can still add new users
        self.assertResponse(response, count=1)
        response = self.makeRequest("/users/login", method="POST", data = user4)        #And this time, we can log in
        self.assertResponse(response, count=2)
        response = self.makeRequest("/users/add", method="POST", data = user2)          # Nothing stopping us from recreating the user
        self.assertResponse(response, count=1)
        response = self.makeRequest("/users/login", method="POST", data = user2)        #Now we can log in again
        self.assertResponse(response, count=2)
        
        

        
class TestAddUser(testLib.RestTestCase):
    """Test adding users"""
    def assertResponse(self, respData, count = 1, errCode = testLib.RestTestCase.SUCCESS):
        """
        Check that the response data dictionary matches the expected values
        """
        expected = { 'errCode' : errCode }
        if count is not None:
            expected['count']  = count
        self.assertDictEqual(expected, respData)

    def testDupeAdd(self):
        """Shouldn't be able to add the same user twice."""
        self.makeRequest("/users/add", method="POST", data = { 'user' : 'user1', 'password' : 'password'} )
        response = self.makeRequest("/users/add", method="POST", data = { 'user' : 'user1', 'password' : 'password'} )
        self.assertResponse(response, count=None, errCode = testLib.RestTestCase.ERR_USER_EXISTS)

    def testLong(self):
        """ Test length checking."""
        longstring = 129 * '*'
        response = self.makeRequest("/users/add", method="POST", data = { 'user' : longstring, 'password' : 'password'} )
        self.assertResponse(response, count=None, errCode = testLib.RestTestCase.ERR_BAD_USERNAME)
        response = self.makeRequest("/users/add", method="POST", data = { 'user' : 'user', 'password' : longstring} )
        self.assertResponse(response, count=None, errCode = testLib.RestTestCase.ERR_BAD_PASSWORD)

    
