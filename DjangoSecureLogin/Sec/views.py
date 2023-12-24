from django.shortcuts import render,redirect
import requests
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .forms import SignUpForm
from .utils import log_activity
from .forms import LoginForm
from .forms import VerifyCodeForm
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required 
import random
from django.contrib.auth.views import PasswordResetCompleteView
from django.contrib.auth import logout

from django.contrib.auth import update_session_auth_hash



import logging

# Create a logger
logger = logging.getLogger(__name__)

def generate_verification_code():
    return str(random.randint(100000, 999999))

def send_verification_code(email, code):
    subject = 'Verification Code'
    message = f'Your verification code is: {code}'
    from_email = 'portfolio.1377@gmail.com'  # Update with your email
    send_mail(subject, message, from_email, [email])

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            print(form.cleaned_data["captcha"])

            user = authenticate(request, username=username, password=password)
            print(user)
            if user is not None:
                verification_code = generate_verification_code()
                send_verification_code(user.email, verification_code)
                # Store the verification code in the session for later verification
                request.session['verification_code'] = verification_code
                log_activity(user, f" user '{user.username}' logged in ")  # Log the user signup
                login(request, user)
                return redirect( 'Sec:verify_code',username=username)
            else:
                messages.error(request, 'Invalid username or password. Please try again.')

    else:
        form = LoginForm()
    
    return render(request, 'login.html', {'form': form})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get('password')
            user.set_password(password)
            user.save()

            log_activity(user, f"New user '{user.username}' signed up")  # Log the user signup

            return redirect('Sec:login')  # Redirect to the login page
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

@login_required
def verify_code(request, username):
    # Check if the user is already authenticated
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = VerifyCodeForm(request.POST)
            if form.is_valid():
                entered_code = form.cleaned_data.get('code')
                stored_code = request.session.get('verification_code')

                if entered_code == stored_code:
                    # Code is valid, perform necessary actions (e.g., log in the user)
                    # ...
                    

                    return redirect('Sec:dashboard')  # Redirect to the dashboard after successful verification
                else:
                    form.add_error('code', 'Invalid code. Please try again.')
        else:
            form = VerifyCodeForm()

        return render(request, 'verify_code.html', {'form': form})
    else:
        # If the user is not authenticated, redirect to the login page
        print('not authneticated')
        return redirect('Sec:login')

@login_required
def dashboard(request):
    # Access the authenticated user's username
    username = request.user.username
    return render(request, 'dashboard.html', {'username': username})




class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    def get(self, request, *args, **kwargs):
        # Customize the redirect logic here
        return redirect('Sec:login')  #
    



def custom_logout(request):
    user=request.user
    log_activity(user, f" user '{user.username}' logged in ")
    logout(request)
    return redirect('Sec:login') 



def landingpage(request):
    return render(request,'landing.html')