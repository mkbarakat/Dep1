import datetime
import re
import bcrypt
from django.db import models
class UserManager(models.Manager):
    def basic_validator(self,post_data):
        errors={}
        if not str(post_data['first_name']).isalpha():
            errors['first_name']="name should be only letters"
        if not str(post_data['first_name']).isalpha():
            errors['last_name']="name should be only letters"
        if len(post_data['first_name'])<2:
            errors['first_name']="First name should be at leaset 2 characters"
        if len(post_data['last_name'])<2:
            errors['last_name']="last name should be at leaset 2 characters"
        if len(post_data['first_name'])<2:
            errors['first_name']="First name should be at leaset 2 characters"
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(post_data['email']):    # test whether a field matches the pattern            
            errors['email'] = "Invalid email address!"
        if len(post_data['password'])<8:
            errors['password']="Password shoul be at least 8 characters"
        if post_data['password']!=post_data['password_confirm']:
            errors['password_confirm']="passwords doesnt match"
        
        if len(User.objects.filter(email=post_data['email']))>0:
            errors['email']=f"this email {(post_data['email'])} is alredy exist" 
        return errors


    def login_validator(self,postDAta):
        errors={}
        user = User.objects.filter(email=postDAta['email'])
        if len(user)==0:
            errors['email']="There is no  user with that email please check your email or go to registration"
        if len(user)==1:
            if not bcrypt.checkpw(postDAta['password'].encode(), user[0].password.encode()):
                errors['password']="Password doesnt match please inseert the correct one"
        return errors



def validate_login(request):
    user = User.objects.get(email=request.POST['email'])  # hm...is it really a good idea to use the get method here?
    return bcrypt.checkpw(request.POST['password'].encode(), user.password.encode())
    


        
class User (models.Model):
    first_name=models.CharField(max_length=255)
    last_name=models.CharField(max_length=255)
    email=models.CharField(max_length=255)
    password=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects=UserManager()
    #messages
    #comments

class Message (models.Model):
    message=models.TextField()
    user=models.ForeignKey(User,related_name="messages",on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    #comments
class Comment(models.Model):
    comment=models.TextField()
    message=models.ForeignKey(Message,related_name="comments",on_delete=models.CASCADE)
    user=models.ForeignKey(User,related_name="comments",on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)




def time_def(message):
    now=datetime.datetime.now()
    post_time=message.created_at
    deff=(now-post_time).total_seconds()/60
    print(deff)
    
