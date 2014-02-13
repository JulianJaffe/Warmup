from django.utils import unittest
from django.test import TestCase
from users.models import User

class UserTestCase(TestCase):

    def test_addUser(self):
        """Make sure that users can be added to the database!"""
        u = User()
        res = u.add("test3", "pass1")
        self.assertEquals(User.SUCCESS, res)

    def test_addExisting(self):
        """Adding an existing user should fail."""
        u = User()
        u.add("test1", "")
        res = u.add("test1", "")
        self.assertEquals(User.ERR_USER_EXISTS, res)

    def test_addTwo(self):
        """Adding two users should work."""
        u = User()
        self.assertEquals(User.SUCCESS, u.add("test1", ""))
        self.assertEquals(User.SUCCESS, u.add("test2", "password"))

    def test_addEmptyUsername(self):
        """Adding a user with no username should fail."""
        u = User()
        self.assertEquals(User.ERR_BAD_USERNAME, u.add("", "pass"))

    def test_userTooLong(self):
        """Adding a username with too many characters should fail."""
        u = User()
        name = "12345678901234567890123456789012345678901234567890" + \
               "12345678901234567890123456789012345678901234567890" + \
               "12345678901234567890123456789012345678901234567890"
        self.assertEquals(User.ERR_BAD_USERNAME, u.add(name, ""))

    def test_passTooLong(self):
        """Adding a password with too many characters should fail."""
        u = User()
        pswd = "12345678901234567890123456789012345678901234567890" + \
               "12345678901234567890123456789012345678901234567890" + \
               "12345678901234567890123456789012345678901234567890"
        self.assertEquals(User.ERR_BAD_PASSWORD, u.add("user", pswd))

    def test_loginIncrement(self):
        """Logging in should increment the login count."""
        u = User()
        u.add("test", "")
        res = u.login("test", "")
        self.assertEquals(2, res)

    def test_badLoginUser(self):
        """Logging in with a non-existent username should fail."""
        u = User()
        self.assertEquals(User.ERR_BAD_CREDENTIALS, u.login("user", ""))

    def test_badLoginPass(self):
        """Logging in with the wrong password should fail."""
        u = User()
        u.add("test", "swordfish")
        self.assertEquals(User.ERR_BAD_CREDENTIALS, u.login("test", ""))

    def test_resetFixture(self):
        """Reseting the database should clear it."""
        u = User()
        u.add("test1", "")
        u.add("test2", "password")
        self.assertEquals(2, u.login("test1", ""))
        self.assertEquals(User.SUCCESS, u.resetFixture())
        self.assertEquals(User.ERR_BAD_CREDENTIALS, u.login("test1", ""))
        self.assertEquals(User.SUCCESS, u.add("test1", ""))
        
