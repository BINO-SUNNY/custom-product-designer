
from django.shortcuts import render,redirect, get_object_or_404
from django.http import JsonResponse
from .models import *
from .forms import *
from customproductdesignerapp.models import users,logins
from django.contrib import messages
from django.contrib.auth import logout
from adminapp.models import *
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Sum
import json


# Create your views here.
def customerhome(request):
    context={
        "categories":Category.objects.all(),
        'products':Products.objects.all(),
        'colors':Color.objects.all()
    }
    return render(request, 'userhome.html',context)
    




def create_design_request(request):
    show_address_modal = False  # Flag to determine if the modal should be opened

    if request.method == "POST":
        form = DesignRequestForm(request.POST, request.FILES)
        address_form = AddressForm(request.POST)  # Handle address data
        gift_form = GiftForm(request.POST)  # Handle gift data
        selected_template_id = request.POST.get("selected_template")  # Get selected template ID

        if form.is_valid() and address_form.is_valid():
            design_request = form.save(commit=False)
            design_request.customer_id = request.session.get('userid')  # Assign customer
            if selected_template_id:
                template = get_object_or_404(Template, id=selected_template_id)
               

                design_request.image = template.image.url  # Assign template image
            design_request.save()


            # If a template is selected, save to RequestedTemplate model
            if selected_template_id:
                requested_template.objects.create(request=design_request, template=template)
                wallet.objects.create(
        customer_id=request.session.get('userid'),  # Assuming `design_request` has a user field
        payed_on=now(),
        request=design_request,
        amount=100  # Or any logic to determine amount
    )

            # Save the address
            address = address_form.save(commit=False)
            address.request = design_request
            address.save()

            # Save gift details if checked
            if request.POST.get("is_gift") == "true":  # Ensure the checkbox is checked
                if gift_form.is_valid():
                    gift = gift_form.save(commit=False)
                    gift.request = design_request
                    gift.save()

            return redirect('customerhome')  # Redirect after successful submission
        else:
            show_address_modal = True # Open modal if address form has errors

    else:
        form = DesignRequestForm()
        address_form = AddressForm()
        gift_form = GiftForm()

    context = {
        'form': form,
        'address_form': address_form,
        'gift_form': gift_form,
        'categories': Category.objects.all(),
        'templates': Template.objects.all(),
        'show_address_modal': show_address_modal,  # Pass flag to template
    }

    return render(request, 'new_design_request.html', context)

# 🟢 Load products dynamically when category is selected
def get_products(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = Products.objects.filter(category=category)

    # Build product data with absolute image URLs
    product_list = []
    for product in products:
        product_list.append({
            'id': product.id,
            'description': product.description,
            'image': request.build_absolute_uri(product.image.url) if product.image else None  # Proper URL handling
        })

    return JsonResponse({'products': product_list})

# 🟢 Load sizes and colors dynamically when product is selected
def get_sizes_colors(request, product_id):
    product = get_object_or_404(Products, id=product_id)
    sizes = Size.objects.all().values('id', 'sizename')
    colors = Color.objects.all().values('id', 'colorname')

    return JsonResponse({'sizes': list(sizes), 'colors': list(colors)})
def get_templates(request):
    templates = Template.objects.all()
    template_list = [
        {
            "id": template.id,
            "image": request.build_absolute_uri(template.image.url),  # Return full URL
        }
        for template in templates
    ]
    return JsonResponse({"templates": template_list})
def myaccount(request):
    # Fetch the logged-in user's details
    user_id=request.session.get('userid')
    user = users.objects.get(id=user_id)  # Assuming the user is logged in and their email is used for lookup
    
    # Fetch user login details
    login_details = logins.objects.get(id=user.login.id)  # We use the ForeignKey to get login details
        

    
    # Fetch all design requests (orders) related to the logged-in user
    my_orders = Design_request.objects.filter(customer_id=user_id)
    
    # Fetch all templates related to the logged-in user
    my_templates = Template.objects.filter(customer_id=user_id)
    notifications = {notify.design_request.id: notify for notify in NotifyDesignRequest.objects.filter(design_request__in=my_orders)}

    # Prepare context for the template
    context = {
        'user_details': user,
        'login_details': login_details,
        'my_orders': my_orders,
        'my_templates': my_templates,
         "notifications": notifications
    }
    print(context)

    # Render the response with the context
    return render(request, 'myaccount.html', context)


def submit_review(request, order_id):
    user_id=request.session.get('userid')
    if request.method == "POST":
        try:
            order = Design_request.objects.get(id=order_id)

            if order.status != "Delivered":
                return JsonResponse({"success": False, "message": "Only delivered orders can be reviewed."})

            rating = request.POST.get("rating")
            review_text = request.POST.get("review_text")

            if not rating or not review_text:
                return JsonResponse({"success": False, "message": "Please provide both a rating and review."})

            # Save Review
            Review.objects.create(order=order,customer_id=user_id, rating=int(rating), review_text=review_text)

            return JsonResponse({"success": True, "message": "Review submitted successfully!"})
        except Design_request.DoesNotExist:
            return JsonResponse({"success": False, "message": "Order not found."})
    return JsonResponse({"success": False, "message": "Invalid request method."})


def cancel_order(request, order_id):
    if request.method == "POST":
        order = get_object_or_404(Design_request, id=order_id)
        order.status = "Cancelled"
        order.save()
        return JsonResponse({"success": True})
    return JsonResponse({"success": False})
def my_templates(request):
    user_id = request.session.get('userid')
    my_templates = Template.objects.filter(customer_id=user_id).prefetch_related("used_by__request__customer")
    return render(request, "my_templates.html", {"my_templates": my_templates})

def fetch_users_for_template(request, template_id):
    try:
        used_templates = requested_template.objects.filter(template_id=template_id).select_related("request__customer")
        users = [{"username": rt.request.customer.name, "order_id": rt.request.id} for rt in used_templates]
        return JsonResponse({"users": users}, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

def delete_template(request, template_id):
    user_id = request.session.get('userid')
    template = get_object_or_404(Template, id=template_id, customer_id=user_id)

    if request.method == "POST":
        template.delete()
        return JsonResponse({"message": "Template deleted successfully."})
    
    return JsonResponse({"error": "Invalid request."}, status=400)
def update_profile(request):
    if request.method == "POST":
        user_id=request.session.get('userid')
        user=users.objects.get(id=user_id)
        user.name = request.POST.get("name")
        user.phno = request.POST.get("phno")
        user.save()
        return JsonResponse({"success": True, "message": "Profile updated successfully!"})
    return JsonResponse({"success": False, "message": "Invalid request"})
def change_password(request):
    if request.method == "POST":
        user_id=request.session.get('userid')
        user=users.objects.get(id=user_id)
        logobj=logins.objects.get(id=user.login_id)
        current_password = request.POST.get("currentPassword")
        new_password = request.POST.get("newPassword")
        confirm_password = request.POST.get("confirmPassword")

        if(current_password!= logobj.password):
            return JsonResponse({"success": False, "message": "Current password is incorrect."})

        if new_password != confirm_password:
            return JsonResponse({"success": False, "message": "New passwords do not match."})

        logobj.password=new_password
        logobj.save()
        logout(request)  # Log out the user after changing password
        return JsonResponse({"success": True, "message": "Password changed successfully!", "redirect": "/login_view/"})
    
    return JsonResponse({"success": False, "message": "Invalid request"})

@csrf_exempt  # Remove this if CSRF token is handled correctly
def update_payment_status(request, order_id):
    try:
        order = Design_request.objects.get(id=order_id)
        order.status = "Payment Completed"
        order.save()
        return JsonResponse({"success": True})
    except Design_request.DoesNotExist:

        return JsonResponse({"success": False, "error": "Order not found"})
import qrcode
from django.http import HttpResponse
from io import BytesIO

def generate_qr(request, order_id):
    order = Design_request.objects.get(id=order_id)
    payment_url = f"https://yourwebsite.com/pay/{order.id}/"  # Replace with actual payment URL
    qr = qrcode.make(payment_url)

    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    return HttpResponse(buffer.getvalue(), content_type="image/png")


def feedback_view(request):
    user_id=request.session.get('userid')
    user=users.objects.get(id=user_id)

    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.customer_id = user_id  # Assuming the user is logged in
            feedback.save()
            
            return redirect('customerhome')  # Redirect to a success page
    else:
        form = FeedbackForm()
    
    return render(request, 'feedback_form.html', {'form': form})




def get_wallet_amount_for_user(request):
    user_id = request.session.get('userid')  # Fetch logged-in user ID
    if not user_id:
        return {'error': 'User not logged in'}

    # Get all templates created by the logged-in user
    user_templates = Template.objects.filter(customer_id=user_id)

    # Get all requested_template entries where the template belongs to the logged-in user
    requested_templates = requested_template.objects.filter(template__in=user_templates)

    # Get all design requests related to those requested templates
    design_request_ids = requested_templates.values_list('request_id', flat=True)

    # Get total wallet amount for the logged-in user as the receiver
    total_amount = wallet.objects.filter(request_id__in=design_request_ids).aggregate(Sum('amount'))['amount__sum'] or 0

    return {'total_wallet_amount': total_amount}

def wallet_view(request):
    """Display the user's wallet balance."""
    wallet_data = get_wallet_amount_for_user(request)
    return render(request, 'wallet.html', wallet_data)

def withdraw_money(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            amount = data.get("amount")

            if not amount or amount < 1000:
                return JsonResponse({"success": False, "message": "Invalid withdrawal amount"}, status=400)

            user_id = request.session.get("userid")
            if not user_id:
                return JsonResponse({"success": False, "message": "User not logged in"}, status=401)

            # Get user's total wallet balance
            total_balance = wallet.objects.filter(customer_id=user_id).aggregate(Sum('amount'))['amount__sum'] or 0

            if total_balance < 1000:
                return JsonResponse({"success": False, "message": "Insufficient balance"}, status=400)

            # Deduct ₹1000, ensuring balance does not go negative
            remaining_balance = max(0, total_balance - 1000)

            # Update wallet records (assuming each entry represents a credited amount)
            wallet_entries = wallet.objects.filter(customer_id=user_id).order_by('payed_on')
            amount_to_deduct = 1000

            for entry in wallet_entries:
                if amount_to_deduct <= 0:
                    break
                if entry.amount <= amount_to_deduct:
                    amount_to_deduct -= entry.amount
                    entry.amount = 0  # Set to zero since it's deducted
                else:
                    entry.amount -= amount_to_deduct
                    amount_to_deduct = 0
                entry.save()

            return JsonResponse({
                "success": True,
                "new_balance": 0,
                "message": "Withdrawal successful!"
            })

        except json.JSONDecodeError:
            return JsonResponse({"success": False, "message": "Invalid JSON data"}, status=400)

    return JsonResponse({"success": False, "message": "Invalid request"}, status=400)



def get_free_templates(request):
    free_templates = FreeTemplate.objects.all()
    free_template_list = [
        {
            "id": template.id,
            "name": template.name,
            "image": request.build_absolute_uri(template.image.url) if template.image else "",
        }
        for template in free_templates
    ]
    return JsonResponse({"templates": free_template_list})



def upload_color_image(request):
    if request.method == 'POST':
        form = UserColorForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('create_design_request')  # Go to your next page
    else:
        form = UserColorForm()

    return render(request, 'new_design_request.html', {'form': form})
