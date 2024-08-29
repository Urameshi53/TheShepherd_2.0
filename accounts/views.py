from datetime import timezone
from typing import Any, Dict
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout
from django.contrib import messages
from django.views import generic
from django.template import RequestContext
import re
from django.core.mail import send_mail
from django.template.loader import render_to_string
import string


from .forms import LoginForm, RegistrationForm, ResetPasswordForm, DiscussionForm
from discussions.models import Student, Discussion

other_error_messages = []

class ProfileView(generic.DetailView):
    template_name = "accounts/profile.html"
    model = Student 

    def get_context_data(self, *args, **kwargs):
        context = super(ProfileView, self).get_context_data(*args, **kwargs)
        context['student'] = Student.objects.filter(user=self.request.user)[0]
        context['discuss_form'] = DiscussionForm
        context['reset_form'] = ResetPasswordForm

        return context

def login(request):
    error_messages = []
    context = {}
    form = LoginForm
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        #user = authenticate(request, email=email, password=password)
        user = None
        for i in User.objects.all():
            if i.email == email and i.check_password(password):
                user = i
                
        if user is not None:
            auth_login(request, user)

            '''if user.is_superuser:
                return redirect('admin')
            else:'''
            return redirect('home')
        else: 
            error_messages.append('Email or password is not correct')
            messages.error(request, 'Username or password does not match')
            print('did not work')
    else:
        pass    

    return render(request, 'accounts/login.html', {'form':form, 'error_messages':error_messages})#, RequestContext(request))


def logout_view(request):
    logout(request)
    return redirect('login')

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
def check_email(email):
    if (re.fullmatch(regex, email)):
        return True 
    else:
        return False
    
def check_password(password, error_messages):
    if re.search('[A-Z]+', password) is None:
        error_messages.append('Password must contain a capital letter')
        return False
    elif re.search('[a-z]+', password) is None:
        error_messages.append('Password must have a small case')
        return False
    elif re.search('[0-9]+', password) is None:
        error_messages.append('Password must include a number')
        return False
    elif re.search('[' + string.punctuation + ']+', password) is None:
        error_messages.append('Password must contain a symbol')
        return False
    elif len(password) < 6:
        error_messages.append('invalid password!')
        return False
    else:
       return True

def signup_view(request):
    error_messages = []
    form = RegistrationForm
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        school = request.POST.get('school')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        users = User.objects.all()
        for i in users:
            if i.email == email:
                error_messages.append('Email already exists')
                return render(request, 'accounts/signup.html', {'form':form, 'error_messages':error_messages})
            if i.username == username:
                error_messages.append('Username already exists')
                return render(request, 'accounts/signup.html', {'form':form, 'error_messages':error_messages})

        if check_password(password1, error_messages):
            if password1 == password2 and check_email(email):
                html_message = render_to_string('accounts/email_message.html')
                message = 'Thank you'
                send_mail(f'Hello {username}, thank you for registering with TheShepherd.', message, 'zigahemmanuel53@gmail.com', [email,], html_message=html_message)

                
                user = User()
                user.username = username
                user.email = email
                user.set_password(password1)
                user.save()

                student = Student()
                student.user = user 
                student.school = school
                student.save()

                auth_login(request, user)
                return render(request, 'accounts/send_email.html')
                #return redirect('home')
            else:
                if password1 != password2:
                    error_messages.append('Passwords do not match')
                else:
                    error_messages.append('Incorrect email')                
    else:
        pass    

    return render(request, 'accounts/signup.html', {'form':form, 'error_messages':error_messages})


def reset_view(request, user_id):
    form = ResetPasswordForm
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        user = User.objects.get(id=user_id)

        if user.check_password(old_password) and password1 == password2:
            user.set_password(password1)
            user.save()    
            #auth_login(request, user)
            return redirect('home')
        else:
            auth_login(request, user)
            if password1 != password2:
                other_error_messages.append('passwords did not match')
            else:
                other_error_messages.append('Old password is wrong')
            return HttpResponseRedirect(f"/accounts/{user_id}/")

def discuss_view(request, user_id):
    form = DiscussionForm
    if request.method == 'POST':
        content = request.POST.get('content')
        description = request.POST.get('description')
        user = User.objects.get(id=user_id)

        discussion = Discussion()
        discussion.content = content 
        discussion.description = description
        student = Student.objects.filter(user=user)[0]
        discussion.creator = student
        discussion.save()

        return HttpResponseRedirect(f"/accounts/{user_id}/")

