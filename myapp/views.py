from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from .forms import CustomUserCreationForm
from django.contrib.auth.models import User

from django.contrib.auth import logout


# Home view (placeholder)
def home(request):
    return render(request, 'home.html')

# Signup view
def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})


# Login view
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, "Invalid username or password")
        else:
            messages.error(request, "Invalid username or password")
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

# views.py
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login
from django.conf import settings
from .forms import CustomUserCreationForm
import random

# Function to generate a random 6-digit OTP
def generate_otp():
    return str(random.randint(100000, 999999))

# Store OTPs temporarily (ideally, store them in the database)
otp_storage = {}

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Don't save the user yet (is_active = False)
            email = form.cleaned_data.get('email')
            otp = generate_otp()  # Generate OTP

            # Store OTP and user data temporarily (could store in session or DB)
            otp_storage[email] = otp
            user.save()

            # Send the OTP to the user's email
            send_mail(
                'Your OTP Code',
                f'Your OTP for verification is {otp}',
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )

            return redirect('otp_verify', email=email)
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})

# views.py
from .forms import OTPForm

def otp_verify(request, email):
    if email not in otp_storage:
        return redirect('signup')

    if request.method == 'POST':
        form = OTPForm(request.POST)
        if form.is_valid():
            entered_otp = form.cleaned_data.get('otp')
            if entered_otp == otp_storage[email]:
                # Activate user account after successful OTP verification
                user = User.objects.get(email=email)
                user.is_active = True
                user.save()

                # Log the user in
                login(request, user)

                # Clear the stored OTP after verification
                del otp_storage[email]

                return redirect('home')
            else:
                form.add_error('otp', 'Invalid OTP. Please try again.')
    else:
        form = OTPForm()

    return render(request, 'otp_verify.html', {'form': form, 'email': email})

