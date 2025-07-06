from django.db import models
from customproductdesignerapp.models import *
from adminapp.models import *
from django.utils.timezone import now 
from django.core.validators import RegexValidator
# Create your models here.
class Design_request(models.Model):
    customer = models.ForeignKey('customproductdesignerapp.users', on_delete=models.CASCADE)
    category = models.ForeignKey('adminapp.Category', on_delete=models.CASCADE)
    product = models.ForeignKey('adminapp.Products', on_delete=models.CASCADE)
    size = models.ForeignKey('adminapp.Size', on_delete=models.CASCADE)
    color = models.ForeignKey('adminapp.Color', on_delete=models.CASCADE)
    request_date = models.DateTimeField(default=now)
    status = models.CharField(max_length=20, default="Pending")
    requestdescription = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='Designimages/', null=True, blank=True)
    add_to_template = models.BooleanField(default=False)  # Checkbox for template addition

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.add_to_template and self.image:  # If checkbox is checked
            Template.objects.create(customer=self.customer, image=self.image)

    def __str__(self):
        return f"Request by {self.customer} - {self.product} ({self.status})"

class Template(models.Model):
    customer = models.ForeignKey('customproductdesignerapp.users',on_delete=models.CASCADE)
    image = models.ImageField(upload_to='Designimages/', null=True, blank=True) 
    def __str__(self):
        return f"Template {self.id} by {self.customer.name}"
class requested_template(models.Model):
    request=models.ForeignKey('design_request',on_delete=models.CASCADE)
    template=models.ForeignKey('template',on_delete=models.CASCADE)
    def __str__(self):
        return f"Template {self.id} by {self.customer.name}"


class Address(models.Model):
    city = models.CharField(max_length=100)  # City name, max length 100
    hname = models.CharField(max_length=255)  # House name, max length 255
    district = models.CharField(max_length=100)  # District name, max length 100
    landmark = models.CharField(max_length=255, blank=True)  # Landmark (optional field)
    pin = models.CharField(max_length=6)  # Postal code, max length 6
    phonenumber = models.CharField(max_length=15)  # Phone number, max length 15
    request = models.ForeignKey('Design_request', on_delete=models.CASCADE)
    pin = models.CharField(
        max_length=6,
        validators=[RegexValidator(r'^\d{6}$', message="Pin code must be exactly 6 digits.")]
    )

    phonenumber = models.CharField(
        max_length=10,
        validators=[RegexValidator(r'^\d{10}$', message="Enter a valid phone number.")]
    )  # Foreign key to Design_request model

    def __str__(self):
        return f"Address in {self.city}, {self.district}, PIN: {self.pin}"
from django.db import models

class Gift(models.Model):
    request = models.ForeignKey('Design_request', on_delete=models.CASCADE)  # Foreign key to Design_request model
    date = models.DateField()  # Date the gift was given or received
    description = models.TextField()  # Detailed description of the gift
    gift_note = models.CharField(max_length=255, blank=True)  # Optional note accompanying the gift

    def __str__(self):
        return f"Gift for request {self.request.id} on {self.date}"


class Review(models.Model):
    order = models.OneToOneField('Design_request', on_delete=models.CASCADE, related_name="review")
    customer = models.ForeignKey('customproductdesignerapp.users', on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])  # Rating from 1 to 5
    review_text = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.customer} for Order {self.order.id} - {self.rating} Stars"

class Feedback(models.Model):
    customer = models.ForeignKey('customproductdesignerapp.users', on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=now)  # Automatically sets the creation timestamp
    comment = models.TextField()  # Stores user feedback

    def __str__(self):
        return f"Feedback by {self.customer.name} on {self.created_at.strftime('%Y-%m-%d')}"


class wallet(models.Model):
    customer = models.ForeignKey('customproductdesignerapp.users', on_delete=models.CASCADE,related_name='wallet_sent')
    request = models.ForeignKey('Design_request', on_delete=models.CASCADE)
    payed_on=models.DateTimeField(default=now)
    amount=models.IntegerField(default=100)

class usercolor(models.Model):
    Color_image = models.ImageField(upload_to='Userimages/', null=True, blank=True) 

    
