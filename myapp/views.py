from django.shortcuts import render,redirect
from .models import *
from django.contrib import messages
from datetime import datetime

import bcrypt

def run(request):
    return render(request,'index.html')

def regester(request):
    errors=User.objects.basic_validator(request.POST)
    if len (errors)>0:
        for key,value in errors.items():
            messages.error(request,value)
        return redirect('/')
    else:
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        email=request.POST['email']
        password=request.POST['password']
        hash1 = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        my_user=User.objects.create(first_name=first_name,last_name=last_name,email=email,password=hash1)
        request.session['current_user_id']=my_user.id
    return redirect('/success')


def login(request):
        errors=User.objects.login_validator(request.POST)
        if len (errors)>0:
            for key,value in errors.items():
                messages.error(request,value)
            if 'current_user_id' in  request.session:
                del request.session['current_user_id']
            return redirect('/')
        else:
            user = User.objects.filter(email=request.POST['email'])
            if user:
                if validate_login(request):
                    logged_user = user[0]
                    request.session['current_user_id']=logged_user .id
                    return redirect('/success')


def success(request):
    if 'current_user_id' in  request.session:
        return redirect('/wall')
    else:
        return redirect('/')

def logout(request):
    del request.session['current_user_id']
    return redirect('/')




def wall (request):
    my_user=User.objects.get(id=request.session['current_user_id'])
    context={
        'messages':Message.objects.all().order_by('-created_at'),
        'current_user':my_user,
    }
    return render(request,'wall.html',context)

def post(request):
    my_message=request.POST['message']
    my_user=User.objects.get(id=request.session['current_user_id'])
    Message.objects.create(message=my_message,user=my_user)
    return redirect('/wall')

def comment(request):
    my_message=Message.objects.get(id=request.POST['message_id'])
    my_user=User.objects.get(id=request.session['current_user_id'])
    my_comment=request.POST['comment']
    Comment.objects.create(comment=my_comment,message=my_message,user=my_user)
    return redirect('/wall')


def dell (request):
    my_comment=Comment.objects.get(id=request.POST['comment_id'])
    my_comment.delete()
    return redirect('/wall')

def dell_post (request):
    my_message=Message.objects.get(id=request.POST['message_id'])
    #################################calculate time difference
    time=datetime.strftime(my_message.created_at,"%Y/%m/%d %H:%M:%S.%f")
    dt2 = datetime.strptime(time, "%Y/%m/%d %H:%M:%S.%f")
    delta = ( datetime.now()-dt2 ).total_seconds()/60
    if delta<30:
        my_message.delete()
    return redirect('/wall')











