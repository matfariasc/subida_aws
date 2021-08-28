from django.db import models

import re

# Create your models here.
def validaremail(email = None, user= None):
    if user:
        email.lower()
        match_email = Users.objects.get(id=user)
        if match_email.email == email:
            print("valide esto")
            return None
    try:
        email.lower()
        match_email = Users.objects.get(email=email)
    except:
        match_email = None
    return match_email
    
class usersManager(models.Manager):
    def basic_validator(self,postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['fname']) < 2:
            errors["fname"] = "El nombre debe tener mas de 2 caractares"
        if len(postData['lname']) < 2:
            errors["lname"] = "El apellido debe tener mas de 2 caractares"
        if not EMAIL_REGEX.match(postData['email']):         
            errors['email'] = "El correo es invalido"
        if postData['password'] != postData['co-password']:
            errors["password"] = "El password no concide"
        if len(postData['password']) <8:
            errors["password"] = "La password debe tener mas de 8 digitos"
        if postData["email"]:
            email = validaremail(email=postData["email"].lower())
            if email:
                errors['email'] = "El correo ya existe"
        return errors

    def basic_validator_updateinfo(self,postData,userid):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['fname']) < 2:
            errors["fname"] = "El nombre debe tener mas de 2 caractares"
        if len(postData['lname']) < 2:
            errors["lname"] = "El apellido debe tener mas de 2 caractares"
        if not EMAIL_REGEX.match(postData['email']):         
            errors['email'] = "El correo es invalido"
        if postData["email"]:
            email = validaremail(email=postData["email"].lower(),user=userid)
            if email:
                errors['email'] = "El correo ya existe"
        return errors
    def basic_validator_updatepw(self,postData):
        errors= {}
        if postData['password'] != postData['co-password']:
            errors["password"] = "El password no concide"
        if len(postData['password']) <8:
            errors["password"] = "La password debe tener mas de 8 digitos"
        return errors
    def basic_validator_updatedesc(self,postData):
        errors= {}
        if len(postData['description']) <5:
            errors["description"] = "La Descripcion debe tener mas de 8 digitos"
        return errors

class Userslevels(models.Model):
    name = models.CharField(max_length=45)
    level = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Users(models.Model):
    first_name = models.CharField(max_length=55)
    last_name = models.CharField(max_length=55)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user_level = models.ForeignKey(Userslevels, related_name="user_level", on_delete=models.CASCADE)
    objects = usersManager()