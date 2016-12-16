from __future__ import unicode_literals

from django.db import models
import bcrypt
import re

# Create your models here.

class validate(models.Manager):
    def validate(self, postData):
        errors = []
        response = {}
        valid_email = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        #see if email is in server, return arror if it is
        if self.filter(email = postData['email']):
            errors.append('**Email already in use**')
        if not len(postData['first_name']) >= 3 or not len(postData['last_name']) >= 3:
            errors.append('**Names must be at least 3 characters**')
        if not len(postData['username']) >= 3:
            errors.append('**Username must be at least 3 characters**')
        if not valid_email.match(postData['email']):
            errors.append('**Please enter a valid email address**')
        if not len(postData['password']) >= 8:
            errors.append('**Password must be at least 8 characters**')
        if not postData['password'] == postData['password_confirmation']:
            errors.append('**Passwords didn\'t match**')
        if errors:
            response['status'] = False
            response['errors'] = errors
        else:
            response['status'] = True
            password = postData['password']
            hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            self.create(first_name = postData['first_name'], last_name = postData['last_name'], email = postData['email'], password = hashed, username = postData['username'], created_at = postData['date'])
        return response

    def login(self, postData):
        errors = []
        response = {}
        user = User.objects.filter(email = postData['email'])
        if not user:
            errors.append('**Email not found. Email is case sensitive. **')
            response['status'] = False
            response['errors'] = errors
            return response
        hashed = user[0].password
        check_password = bcrypt.hashpw(postData['password'].encode('utf-8'), hashed.encode('utf-8'))
        if not hashed == check_password:
            errors.append('**Incorrect password**')
            response['status'] = False
            response['errors'] = errors
        else:
            response['status'] = True
        return response

class User(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    username = models.CharField(max_length=255, default = "User")
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    apdated_at = models.DateTimeField(auto_now = True)
    objects = validate()
