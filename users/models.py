from django.db import models
from django.core.exceptions import ObjectDoesNotExist

# Create your models here.
class User(models.Model):
    """ """
    ## The success return code
    SUCCESS = 1

    ## Cannot find the user/password pair in the database (for login only)
    ERR_BAD_CREDENTIALS = -1

    ## trying to add a user that already exists (for add only)
    ERR_USER_EXISTS = -2

    ## invalid user name (empty or longer than MAX_USERNAME_LENGTH) (for add, or login)
    ERR_BAD_USERNAME = -3

    ## invalid password name (longer than MAX_PASSWORD_LENGTH) (for add)
    ERR_BAD_PASSWORD = -4
    
    ## The maximum length of user name
    MAX_USERNAME_LENGTH = 128

    ## The maximum length of the passwords
    MAX_PASSWORD_LENGTH = 128

    username = models.CharField(unique = True, max_length = MAX_USERNAME_LENGTH)
    pwd = models.CharField(max_length = MAX_PASSWORD_LENGTH, blank=True)
    count = models.IntegerField(default=1)

    def add(self, user, password):
        """Adds user USER with password PASSWORD to the database, or returns
        a negative error code."""
        if user == '' or len(user) > User.MAX_USERNAME_LENGTH:
            return User.ERR_BAD_USERNAME
        elif len(password) > User.MAX_PASSWORD_LENGTH:
            return User.ERR_BAD_PASSWORD
        else:
            try:
                query = User.objects.get(username=user)
                return User.ERR_USER_EXISTS
            except User.DoesNotExist:
                q = User(username=user, pwd=password)
                q.save()
                return User.SUCCESS

    def login(self, user, password):
        """Increments the login count for user USER or returns a negative error
        code if USER does not exist or has a different password than PASSWORD."""
        try:
            query = User.objects.get(username = user)
            if query.pwd == password:
                count = query.count + 1
                query.count = count
                query.save()
                return count
            else:
                return User.ERR_BAD_CREDENTIALS
        except ObjectDoesNotExist:
            return User.ERR_BAD_CREDENTIALS

    def resetFixture(self):
        """Clears the database and returns success."""
        query = User.objects.all()
        query.delete()
        return User.SUCCESS

    def unitTests(self):
        """Runs the unit tests and returns the vital information."""
        import subprocess
        import re
        noFailed = -1
        noTests = -1
        try:
            output = subprocess.check_output(["python", "manage.py", "test"], stderr = subprocess.STDOUT, universal_newlines = True)
            tests = re.compile("Ran (\d+) tests",re.MULTILINE)
            print tests
            r = tests.search(output)
            if r:
                noTests = r.group(1)
            else:
                noTests = 0
            failed = re.compile("FAILED (.+)",re.MULTILINE)
            r = failed.search(output)
            if r:
                failed = re.findall('\d+', r.group(1))
                noFailed = 0
                for num in failed:
                    try:
                        noFailed += int(num)
                    except ValueError:
                        continue
            else:
                noFailed = 0
        except subprocess.CalledProcessError, e:
            output = e.output
            print e.cmd, e.returncode
        return noFailed, output, noTests
    
