from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.models import User, auth

# handle sign up page requests
def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['fname']
        last_name = request.POST['lname']
        email = request.POST['email']
        password = request.POST['pass']
        re_password = request.POST['re_pass']

        if password == re_password:
            if not User.objects.filter(username=username).exists():
                if not User.objects.filter(email=email).exists():
                    user = User.objects.create_user(username=username,
                                                    password=password,
                                                    email=email,
                                                    first_name=first_name,
                                                    last_name=last_name)
                    user.save()
                    messages.info(request,'Successfully resigtered ..')
                    return redirect('/login/signin')
                else:
                    messages.error(request,'This email is already registered')
                    return redirect('/login/signup')
            else:
                messages.error(request,'Username is already present')
                return redirect('/login/signup')
        else:
            messages.error(request,'Password not matched')
            return redirect('/login/signup')

    return render(request,'signup.html')

# handle sign in page requets
def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['pass']

        user = auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request,user)
            return redirect('/dashboard/home')
        else:
            messages.error(request,'Invalid credientials')
            return redirect('/login/signin')

    return render(request,'signin.html')

# handle logout
def logout(request):
    auth.logout(request)
    return redirect('/login/signin')


