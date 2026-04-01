from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from doctors.models import Doctor
from django.contrib.auth.models import User
from .models import Patient,Registration
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect, csrf_exempt

def register(request):
    if request.method == "POST":
        name = request.POST['patientname']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        gender = request.POST['gender']
        blood_group = request.POST['bloodgroup']
        phone = request.POST['mobile']
        address = request.POST['address']

        # check Password  
        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect('register')

        
        username = email  

        #  Check if user already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "User already registered with this email")
            return redirect('register')

        # Create User
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        Patient.objects.create(
            user=user,
            name=name,
            gender=gender,
            blood_group=blood_group,
            phone=phone,
            address=address
        )

        messages.success(request, "Registration successful. Please login.")
        return redirect('login')

    return render(request, 'patient_register.html')

@csrf_exempt
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")  
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            if hasattr(user, "doctor"):
                return redirect("doctor_dashboard")
            else:
                return redirect("index")

        return render(request, "login.html", {
            "error": "Invalid username or password"
        })

    return render(request, "login.html")

def home(request):
    return render(request, "index.html")

def about(request):
    return render(request, "about.html")

def services(request):
    return render(request, "services.html")

def contact(request):
    return render(request, "contact.html")

def logout_view(request):
    logout(request)
    return redirect('login')

def service_details(request, name):
    return render(request, 'service_details.html', {
        'service': name
    })

def login_redirect(request):
    if request.user.is_authenticated:
        if hasattr(request.user, 'doctor'):
            return redirect('doctor_dashboard')
        else:
            return redirect('index')

    return redirect('login')