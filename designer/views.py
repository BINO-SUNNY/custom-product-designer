from django.shortcuts import render,redirect,get_object_or_404
from customer.models import Design_request,Gift,Address
from adminapp.models import NotifyDesignRequest,Designers
from django.http import JsonResponse  # <-- Add this at the top
from designer.forms import DesignerProfileForm 
from adminapp.forms import DesignerForm
from customproductdesignerapp.models import logins


# Create your views here.

def designerdashboard(request):
    designerid = request.session.get('designerid')

    # Get the designer associated with the logged-in user
    designer = get_object_or_404(Designers, id=designerid)

    # Fetch latest notifications (limit to 5)
    notifications = NotifyDesignRequest.objects.filter(
        designer=designer, 
        design_request__status='Payment Completed'
    ).order_by('-id')[:5]

    context = {
        'designer': designer,
        'notifications': notifications  # Pass notifications to template
    }
    return render(request, 'designerhome.html', context)

def allocated_jobs(request):
    """
    View to display allocated jobs for the logged-in designer.
    Jobs with status 'Payment Completed' are shown.
    """
    designerid = request.session.get('designerid')
    designer = get_object_or_404(Designers, id=designerid)

    # Fetch all NotifyDesignRequest records for this designer
    notify_requests = NotifyDesignRequest.objects.filter(
        designer=designer, 
        design_request__status='Payment Completed'
    ).select_related('design_request')

    allocated_jobs = []
    for notify in notify_requests:
        job = notify.design_request
        job.expected_date = notify.expected_date  # Attach expected date from NotifyDesignRequest
        job.amount = notify.amount  # Attach amount from NotifyDesignRequest

        # Fetch additional details: Address & Gifts
        job.address = job.address if hasattr(job, 'address') else None
        job.gifts = Gift.objects.filter(request=job)
        
        allocated_jobs.append(job)

    context = {
        'allocated_jobs': allocated_jobs,
    }
    return render(request, 'allocated.html', context)


def completed_jobs(request):
    """
    View to display completed jobs for the logged-in designer.
    Jobs with status 'Delivered' are shown.
    """
    designerid = request.session.get('designerid')
    designer = get_object_or_404(Designers, id=designerid)

    completed_jobs = Design_request.objects.filter(
        id__in=NotifyDesignRequest.objects.filter(
            designer=designer, design_request__status='Delivered'
        ).values_list('design_request_id', flat=True)
    )

    context = {
        'completed_jobs': completed_jobs,
    }
    return render(request, 'completed.html', context)



def change_order_status(request, order_id):
    """
    View to change the status of a job to 'Delivered'.
    """
    order = get_object_or_404(Design_request, id=order_id)
    order.status = 'Delivered'
    order.save()
    return redirect('allocated_jobs')  # Redirect to allocated jobs or another page


def get_notifications(request):
    """
    View to fetch new notifications dynamically when the user clicks the notification icon.
    """
    designerid = request.session.get('designerid')
    designer = get_object_or_404(Designers, id=designerid)

    notifications = NotifyDesignRequest.objects.filter(
        designer=designer, 
        design_request__status='Payment Completed'
    ).order_by('-id')[:5]

    notification_list = [
        {
            'description': notification.design_request.product.description,
            'customer_name': notification.design_request.customer.name
        }
        for notification in notifications
    ]

    return JsonResponse({'notifications': notification_list, 'count': len(notification_list)})   

def profile(request):
    designerid = request.session.get('designerid')
    designer = get_object_or_404(Designers, id=designerid)

    if request.method == "POST":
        form = DesignerProfileForm(request.POST, request.FILES, instance=designer)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True, "message": "Profile updated successfully!"})
        return JsonResponse({'errors': form.errors}, status=400)

    form = DesignerProfileForm(instance=designer)
    return render(request, 'profile.html', {'form': form})



from django.shortcuts import render


from django.shortcuts import render
from django.db.models import Sum

def notify_design_requests_list(request):
    # Filter NotifyDesignRequest by designer (based on session)
    designer_id = request.session.get('designerid')
    
    if designer_id:
        notify_design_requests = NotifyDesignRequest.objects.filter(designer_id=designer_id)
    else:
        notify_design_requests = NotifyDesignRequest.objects.none()  # No records if designer_id is not in session

    # Calculate total credit
    total_credit = notify_design_requests.aggregate(Sum('credit'))['credit__sum'] or 0  # Get the sum of credit, or 0 if no records
    
    # Paginate the results if needed
    from django.core.paginator import Paginator
    paginator = Paginator(notify_design_requests, 10)  # Show 10 items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'notify_design_requests.html', {'page_obj': page_obj, 'total_credit': total_credit})


