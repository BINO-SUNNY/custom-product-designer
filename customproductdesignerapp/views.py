from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from adminapp.models import *
from .forms import *
from .models import *
from customer.models import Template,Design_request

def index(request):
    obj=Category.objects.all()
    context={
        "categories":Category.objects.all()

    }
    return render (request,'index.html',context)
    

def login_view(request):
    context={
        "categories":Category.objects.all(),
        'products':Products.objects.all(),
        'colors':Color.objects.all(),
        'templates':Template.objects.all()
    }
    if request.method == 'POST':
        form = LoginForm(request.POST)
        
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            # Check if the email exists in the tblUser_Log (login table)
            try:
                user_log = logins.objects.get(email=email)
            except logins.DoesNotExist:
                form.add_error('email', 'Email does not exist')
                return render(request, 'userlogin.html', {'form': form})
            
            # Check if the password matches
            if user_log.password != password:
                form.add_error('password', 'Incorrect password')
                return render(request, 'userlogin.html', {'form': form})
            
            # Determine the user type (client, advocate, or admin)
            user = None
            
            if user_log.user_type == 'user':
                try:
                    user = users.objects.get(login_id=user_log.id)
                except users.DoesNotExist:
                    form.add_error('email', 'Client account not found.')
                    return render(request, 'userlogin.html', {'form': form})
                # Redirect to client dashboard or appropriate page
                request.session['userid'] = user.id
                return render(request, 'userhome.html',context)

            if user_log.user_type == 'Designer':
                try:
                    designer = Designers.objects.get(login_id=user_log.id)
                except designer.DoesNotExist:
                    form.add_error('email', 'Designer account not found.')
                    return render(request, 'userlogin.html', {'form': form})
                    
                # Redirect to client dashboard or appropriate page
                request.session['designerid'] = designer.id
                return redirect('designerdashboard')

           

            elif user_log.user_type == 'admin':
                # Handle admin login and redirect to admin home
                return render(request, 'admindex.html')

            # If user is not found or keyuser is unrecognized
            form.add_error('email', 'Invalid user type or account.')
            return render(request, 'login.html', {'form': form})

    
        

    return render(request, 'userlogin.html')
def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login_view')  # Redirect after successful registration
    else:
        form = RegistrationForm()
    
    return render(request, "register.html", {"form": form})

def about(request):
    return render(request, 'about.html') 

def contact(request):
    return render(request,'contact.html')

from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.contrib import messages
from customproductdesigner import settings

def forget_link(request):
    if request.method == "POST":
        email = request.POST.get("email")
        user = logins.objects.filter(email=email).first()  

        if user:
            reset_link = f"http://127.0.0.1:8000/new_pass?email={user.email}"
            subject = "Password Reset Request"
            message = f"Click the link to reset your password: {reset_link}"
            send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)

            messages.success(request, f"A password reset link has been sent to {user.email}.")
            return redirect("redirectt")

        messages.error(request, "Email not found.")

    return render(request, "forget_link.html")


def new_pass(request):
    email = request.GET.get("email")  # Get email from URL

    if not email:
        messages.error(request, "Invalid password reset link.")
        return redirect("forget_link")

    user = logins.objects.filter(email=email).first()
    if not user:
        messages.error(request, "User not found.")
        return redirect("forget_link")

    if request.method == "POST":
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        if new_password == confirm_password:
            user.password = new_password # Securely set the new password
            user.save()
            messages.success(request, "Your password has been updated successfully. Please log in.")
            return redirect("login_view")  # Redirect to login

        messages.error(request, "Passwords do not match. Please try again.")

    return render(request, "email_template.html", {"email": email})



def redirectt(request):
    return render(request, "redirect.html")