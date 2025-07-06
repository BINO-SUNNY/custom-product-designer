#from django.shortcuts import render
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import *
from .forms import  *
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import logout
from customer.models import *

# Create your views here.
def admindex(request):
    stats = {
        "new_requests": 32,
        "completed_requests": 120,
        "active_designers": 8,
    }
    return render(request, 'admindex.html', {'stats': stats})

def adminnav(request):
    return render(request,'adminnav.html')    
# View to list all categories
def category_list(request):
    categories = Category.objects.all()
    
    return render(request, 'category.html', {'categories': categories, 'form': CategoryForm()})

# View to add a new category
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        print(form.errors)
        if form.is_valid():
            form.save()
            return redirect('category_list')  # Redirect to the category list after adding
    return redirect('category_list')  # If it's a GET request, just redirect to the list

# View to delete a category
def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    
   
    category.delete()
    return redirect('category_list')  # Redirect back to the category list after deletion

    return HttpResponse(status=405) 
    
def color_list(request):
    colors = Color.objects.all()
    
    if request.method == 'POST':
        form = ColorForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('color_list')  # Redirect to color list after adding
    else:
        form = ColorForm()  # Empty form to add a new color
    
    return render(request, 'color.html', {'colors': colors, 'form': form})

# View to delete a color
def delete_color(request, color_id):
    color = get_object_or_404(Color, id=color_id)
    color.delete()
    return redirect('color_list')
#view to add size

def size_list(request):
    sizes = Size.objects.all()
    
    if request.method == 'POST':
        form = SizeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('size_list')  # Redirect to color list after adding
    else:
        form = SizeForm()  # Empty form to add a new color
    
    return render(request, 'size.html', {'sizes': sizes, 'form': form})

# View to delete a color
def delete_size(request, size_id):
    size = get_object_or_404(Size, id=size_id)
    size.delete()
    return redirect('size_list')

  #view to products list  

def products_list(request):
    products = Products.objects.all()
    return render(request, 'product_list.html', {'products': products})

# View to add a new product
def add_product(request):
    if request.method == 'POST':
        form = ProductsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('products_list')  # Redirect to the products list page
    else:
        form = ProductsForm()
    
    return render(request, 'add_product.html', {'form': form})

# View to delete a product
def delete_product(request, product_id):
    product = Products.objects.get(id=product_id)
    product.delete()
    return redirect('products_list')  # Redirect to the products list page
#designer
def designer_list(request):
    form = DesignerForm()  # Make sure the form is passed
    designers = Designers.objects.all()  # Query your designers
    return render(request, 'designer_list.html', {'form': form, 'designers': designers})

def add_designer(request):
    if request.method == 'POST':
        form = DesignerForm(request.POST, request.FILES)
        print(form.errors)
        print(request.POST)
        print(request.FILES)


        if form.is_valid():
            form.save()
            return redirect('designer_list')
    else:
        form = DesignerForm()
    return render(request, 'designer_form_modal.html', {'form': form})




def edit_designer(request, designer_id):
    """Fetch or update designer details."""
    designer = get_object_or_404(Designers, id=designer_id)

    if request.method == "POST":
        # Update designer details
        designer.name = request.POST.get("name")
        designer.phonenumber = request.POST.get("phonenumber")
        designer.qualification = request.POST.get("qualification")
        designer.description = request.POST.get("description")

        # Handle photo upload
        if "photo" in request.FILES:
            designer.photo = request.FILES["photo"]

        designer.save()
        return JsonResponse({"message": "Designer updated successfully!"})

    # If it's a GET request, return JSON response
    data = {
        "name": designer.name,
        "phonenumber": designer.phonenumber,
        "qualification": designer.qualification,
        "description": designer.description,
        "photo_url": designer.photo.url if designer.photo else None
    }
    return JsonResponse(data)


def delete_designer(request, pk):
    designer = get_object_or_404(Designers, pk=pk)
    designer.delete()
    return redirect('designer_list')

def get_designer_details(request, designer_id):
    """Fetch designer details and return as JSON."""
    designer = get_object_or_404(Designers, id=designer_id)

    data = {
        "name": designer.name,
        "phonenumber": designer.phonenumber,
        "qualification": designer.qualification,
        "description": designer.description,
        "photo_url": designer.photo.url if designer.photo else None
    }
    
    return JsonResponse(data)
def logout_view(request):
    logout(request)
    return redirect('login_view')


def newrequest(request):
    # Fetch all Design requests (you can also filter them if needed)
    design_requests = Design_request.objects.filter(status="Pending")

    # Pass the data to the template
    return render(request, 'newrequest.html', {'design_requests': design_requests})




def design_request_detail_view(request, request_id):
    # Get the design request object by ID (it will return a 404 if not found)
    design_request = get_object_or_404(Design_request, id=request_id)
    designerlist=Designers.objects.all()
    # Optional: Retrieve related objects like Address and Gifts if they exist
    address = design_request.address if hasattr(design_request, 'address') else None
    gifts = Gift.objects.filter(request=design_request)
    print(designerlist)
    # Pass the data to the template
    return render(
        request,
        'design_request_detail.html',
        {
            'design_request': design_request,
            'address': address,
            'gifts': gifts,
            'designers':designerlist
        }
    )
def notify_design_request_create(request):
    if request.method == 'POST':
        design_request_id = request.POST.get('design_request_id')
        expected_date = request.POST.get('expected_date')
        amount = request.POST.get('amount')
        designer_id=request.POST.get('designer_id')

        # Get the DesignRequest object
        design_request = get_object_or_404(Design_request, id=design_request_id)

        # Create the NotifyDesignRequest object
        notify = NotifyDesignRequest(
            design_request=design_request,
            expected_date=expected_date,
            amount=amount,designer_id=designer_id
        )
        notify.save()

        # Update the status of the DesignRequest to "On Process"
        design_request.status = 'On Process'
        design_request.save()

        return JsonResponse({'success': True})

    return JsonResponse({'success': False}, status=400)



def orders_on_process(request):
    # Fetch orders with status 'On Process'
    orders_on_process = Design_request.objects.filter(status='On Process')

    # Fetch notifications related to these orders
    notifications = {n.design_request.id: n for n in NotifyDesignRequest.objects.filter(design_request__in=orders_on_process)}

    # Fetch address details for orders
    addresses = {addr.request.id: addr for addr in Address.objects.filter(request__in=orders_on_process)}

    # Fetch gift details for orders
    gifts = {gift.request.id: gift for gift in Gift.objects.filter(request__in=orders_on_process)}

    return render(request, 'request_onprocess.html', {
        'orders_on_process': orders_on_process,
        'notifications': notifications,  # Pass notifications
        'addresses': addresses,  # Pass addresses
        'gifts': gifts  # Pass gifts
    })


def payment_completed(request):
    # Fetch orders with status 'On Process'
    payment_completed = Design_request.objects.filter(status='Payment Completed')

    return render(request, 'payment_completed.html', {'payment_completed': payment_completed})



def completed_orders(request):
    # Fetch orders with status 'On Process'
    orders_on_process = Design_request.objects.filter(status='Delivered')

    # Fetch notifications related to these orders
    notifications = {n.design_request.id: n for n in NotifyDesignRequest.objects.filter(design_request__in=orders_on_process)}

    # Fetch address details for orders
    addresses = {addr.request.id: addr for addr in Address.objects.filter(request__in=orders_on_process)}

    # Fetch gift details for orders
    gifts = {gift.request.id: gift for gift in Gift.objects.filter(request__in=orders_on_process)}

    return render(request, 'request_onprocess.html', {
        'orders_on_process': orders_on_process,
        'notifications': notifications,  # Pass notifications
        'addresses': addresses,  # Pass addresses
        'gifts': gifts  # Pass gifts
    })
def cancelled_orders(request):
    # Fetch orders with status 'On Process'
    orders_on_process = Design_request.objects.filter(status='Cancelled')

    # Fetch notifications related to these orders
    notifications = {n.design_request.id: n for n in NotifyDesignRequest.objects.filter(design_request__in=orders_on_process)}

    # Fetch address details for orders
    addresses = {addr.request.id: addr for addr in Address.objects.filter(request__in=orders_on_process)}

    # Fetch gift details for orders
    gifts = {gift.request.id: gift for gift in Gift.objects.filter(request__in=orders_on_process)}

    return render(request, 'request_onprocess.html', {
        'orders_on_process': orders_on_process,
        'notifications': notifications,  # Pass notifications
        'addresses': addresses,  # Pass addresses
        'gifts': gifts  # Pass gifts
    })




def customer_templates(request):
    """Fetch all templates added by customers."""
    templates = Template.objects.all()  # Fetch all templates
    return render(request, "view_templates.html", {"templates": templates})

def delete_template(request, template_id):
    """Delete a specific template."""
    template = get_object_or_404(Template, id=template_id)
    template.delete()
    return JsonResponse({"message": "Template deleted successfully!"})

def customer_reviews(request):
    """Fetch all customer reviews."""
    reviews = Review.objects.select_related("customer", "order").all()  # Fetch all reviews
    return render(request, "view_reviews.html", {"reviews": reviews})
    
    
from django.shortcuts import render, redirect, get_object_or_404
from .models import FreeTemplate
from .forms import FreetemplateForm

# View to display list of free templates
def free_template_list(request):
    templates = FreeTemplate.objects.all()
    form = FreetemplateForm()
    return render(request, 'free_template.html', {'free_template': templates, 'form': form})

# View to add a new free template
def add_free_template(request):
    if request.method == 'POST':
        form = FreetemplateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        else:
            print("Form errors:", form.errors)
    return redirect('free_template_list')  # Whether valid or not, redirect back to the template list

# View to delete a free template
def delete_free_template(request, free_template_id):
    template = get_object_or_404(FreeTemplate, id=free_template_id)
    template.delete()
    return redirect('free_template_list')


def customer_feedbacks(request):
    """Fetch all customer feedback."""
    feedbacks = Feedback.objects.select_related("customer").all().order_by("-created_at")
    return render(request, "feedbacks.html", {"feedbacks": feedbacks})
