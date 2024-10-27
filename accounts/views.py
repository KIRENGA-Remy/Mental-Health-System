# from django.shortcuts import render
# from .models import users_collection
# from django.http import HttpResponse

# # Create your views here.
# from django.shortcuts import render, redirect
# from django.contrib.auth import authenticate, login
# from django.contrib import messages

# def index(request):
#     return HttpResponse("<h1>App is running...</h1>")

# def add_user(request):
#     records = {
#         "first_name":"John",
#         "last_name":"smith"
#     }
#     users_collection.insert_one(records)
#     return HttpResponse("New user is added")

# def get_users(request):
#     users=users_collection.find()
#     return HttpResponse(users)

# def login_view(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#         user = authenticate(request, username=email, password=password)
#         if user is not None:
#             login(request, user)
#             return redirect('home')  # Redirect to a home page after login
#         else:
#             messages.error(request, 'Invalid email or password.')
#     return render(request, 'accounts/login.html')





from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import users_collection

def index(request):
    return HttpResponse("<h1>App is running...</h1>")

def add_user(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        records = {"first_name": first_name, "last_name": last_name}
        users_collection.insert_one(records)
        return HttpResponse("New user is added")
    return render(request, 'accounts/add_user.html')


def get_users(request):
    users = list(users_collection.find({}, {"_id": 0, "first_name": 1, "last_name": 1}))
    return JsonResponse(users, safe=False)

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Ensure 'home' view is defined
        else:
            messages.error(request, 'Invalid email or password.')
    return render(request, 'accounts/login.html')
