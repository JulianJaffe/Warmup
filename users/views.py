from django.shortcuts import render
from django.http import HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt
from users.models import User

def index(request):
    return render(request, 'users/index.html')

@csrf_exempt
def login(request):
    """Attempts to login with the provided credentials, and returns a json object with either the
    login count and errCode = User.SUCCESS, or a failing error code."""
    user = User()
    b = request.body
    jsonrequest = json.loads(b.replace("\'",''))
    username = jsonrequest['user']
    password = jsonrequest['password']
    result = {}
    res = user.login(username, password)
    if res > 0:
        result['errCode'] = User.SUCCESS
        result['count'] = res
    else:
        result['errCode'] = res
    return HttpResponse(json.dumps(result), content_type="application/json")

@csrf_exempt
def addUser(request):
    """Attempts to add a user with the provided credentials to the database and returns a json
    object with either a successful error code and count = 1 or a failing error code."""
    user = User()
    b = request.body
    jsonrequest = json.loads(b.replace("\'",''))
    result = {}
    username = jsonrequest['user']
    password = jsonrequest['password']
    errCode = user.add(username, password)
    result['errCode'] = errCode
    if errCode > 0:
        result['count'] = 1
    return HttpResponse(json.dumps(result), content_type="application/json")

@csrf_exempt
def resetFixture(request):
    """Resets the database of users and returns a json object with a successful error code."""
    user = User()
    result = {'errCode': user.resetFixture()}
    return HttpResponse(json.dumps(result), content_type="application/json")

@csrf_exempt
def unitTests(request):
    """Runs all the unit tests and returns a json object with the total number of tests run, their
    output, and the number of failed tests."""
    user = User()
    res = user.unitTests()
    result = {'nrFailed': res[0], 'output': res[1], 'totalTests': res[2]}
    return HttpResponse(json.dumps(result), content_type="application/json")
    
    
        
