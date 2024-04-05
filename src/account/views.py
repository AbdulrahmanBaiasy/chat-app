from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, login, authenticate
from django.contrib import messages


from .forms import LoginForm, RegisterUserForm

# Create your views here.

User = get_user_model()


def login_auth(request):
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = request.POST.get("email")
            password = request.POST.get("password")
            user = authenticate(request, email=email, password=password)
            if user:
                login(request, user)
                return redirect("app:index")
            else:
                messages.error(request, "Invalid email or password ")
        else:
            print("form is not valid", form.errors)
    context = {"form": form}
    return render(request, "account/login.html", context)


def register(request):
    form = RegisterUserForm()
    if request.method == "POST":
        form = RegisterUserForm(request.POST)

        if form.is_valid():
            try:
                user = form.save()
                user.set_password(request.POST["password"])
                user.save()
                return redirect("/login")
            except Exception as e:
                messages.error(request, f"An error occurred during registration: {e}")
            else:
                messages.error(request, "Please correct the errors below.")
        else:
            print("form is not valid", form.errors)

    return render(request, "account/register.html", {"form": form})
