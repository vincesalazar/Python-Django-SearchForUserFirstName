from django.shortcuts import render, redirect
from django.contrib import messages
import bcrypt
from .models import User

def index(request):
    return render(request, 'logReg.html');

def loginUser(request):
    post = request.POST
    try:
        user = User.objects.get(email = post['email']);
    except:
        messages.error(request, "Please check your password or email.")
        return redirect('/login');

    if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
        request.session["user_id"] = user.id
        return redirect('/dash');
    
    messages.error(request, "please check your password or email.")
    return redirect('/');

def regUser(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/');
    if User.objects.filter(user_name = request.POST['user_name']).exists():
        messages.error(request, "username already exists")
        return redirect('/')
    if User.objects.filter(email = request.POST['email']).exists():
        messages.error(request, "email already exists")
        return redirect('/')
    else:
        post = request.POST
        password = post['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        if len(post['desc']) > 1:
            user = User.objects.create(
            user_name = post['user_name'],
            first_name = post['first_name'].capitalize(), 
            last_name = post['last_name'].capitalize(), 
            email = post['email'].lower(), 
            password = pw_hash,
            description = post['desc'],
            )
            request.session['user_id'] = user.id

            return redirect('/dash')
        user = User.objects.create(
            user_name = post['user_name'],
            first_name = post['first_name'].capitalize(), 
            last_name = post['last_name'].capitalize(), 
            email = post['email'].lower(), 
            password = pw_hash,
            description = post['default_desc'],
            )
        request.session['user_id'] = user.id

        return redirect('/dash')

def dash(request):
    if 'user_id' not in request.session:
        return redirect('/');
    if 's_first_name' not in request.session:
        print("name not in session")
        context={
            "user": User.objects.get(id=request.session['user_id']),
        }
        return render(request, 'dash.html', context);
    
    print("name is in session")
    context = {
        "user": User.objects.get(id=request.session['user_id']),
        "searchedUsers": User.objects.filter(first_name = request.session['s_first_name'].capitalize()),
    }
    return render(request, "dash.html", context);

def findByFirstName(request):
    post = request.POST
    print(User.objects.filter(first_name = post['first_name'].capitalize()).exists())
    if User.objects.filter(first_name = post['first_name'].capitalize()).exists():
        if 's_first_name' in request.session:
            del request.session['s_first_name'];
        print(post['first_name'])
        request.session['s_first_name'] = post['first_name'].capitalize();
        return redirect('/dash')
    messages.error(request, 'No users with that first name.')
    if 's_first_name' in request.session:
        del request.session['s_first_name'];
    return redirect('/dash');