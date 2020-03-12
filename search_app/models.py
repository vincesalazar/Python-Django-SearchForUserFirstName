from __future__ import unicode_literals
import re
from django.db import models

class UserManager(models.Manager):
    def basic_validator(self, post_data):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        if len(post_data['user_name']) < 3:
            errors['user_name'] = "User name must be longer than 3 letters."
        if len(post_data['first_name']) < 2:
            errors['first_name'] = "Please provide a first name at least 2 letters long."
        if len(post_data['last_name']) < 2:
            errors['last_name'] = "Please provide a last name at least 2 letters long."
        if len(post_data['email']) < 1:
            errors['email'] = "Please provide a email."
        if not EMAIL_REGEX.match(post_data['email']):            
            errors['email'] = "Invalid email address!"
        if len(post_data['password']) < 3:
            errors['password'] = "Please provide a password at least 3 letters"
        if post_data['pw_confirm'] != post_data['password']:
            errors['pw_confirm'] = "Password confirmation doesn't match"
        return errors

class User(models.Model):
    user_name = models.CharField(max_length=25)
    first_name = models.CharField(max_length = 25)
    last_name = models.CharField(max_length = 25)
    email = models.EmailField()
    password = models.CharField(max_length = 64)
    description = models.CharField(default="Classified" ,max_length = 255)

    created_at = models.DateTimeField(auto_now = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = UserManager()
