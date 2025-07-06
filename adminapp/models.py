from django.db import models
from customproductdesignerapp.models import logins 
from customer.models import Design_request
# Create your models here.
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=254)
    image = models.ImageField(upload_to='category_images/', null=True, blank=True)  # Store images in the 'category_images' folder

    def __str__(self):
        return self.name
class Color(models.Model):
    colorname = models.CharField(max_length=254)
   # image = models.ImageField(upload_to='color_images/', null=True, blank=True)
class Size(models.Model):
    sizename = models.CharField(max_length=254)
class Products(models.Model):
    category = models.ForeignKey("Category", on_delete=models.CASCADE)
    image = models.ImageField(upload_to='color_images/', null=True, blank=True)  
    description=models.TextField()  
 # Ensure correct import

class Designers(models.Model):
    name = models.CharField(max_length=255)  # Full name
    login = models.ForeignKey(logins, on_delete=models.CASCADE)  # Link to logins table
    phonenumber = models.CharField(max_length=15)  # Phone number
    qualification = models.CharField(max_length=255)  # Educational qualification
    description = models.TextField()  # Designer bio/description
    photo = models.ImageField(upload_to='designer_photos/', blank=True, null=True)  # Profile photo

    def __str__(self):
        return self.name


from decimal import Decimal, InvalidOperation
from django.utils import timezone  # To get the current date

class NotifyDesignRequest(models.Model):
    design_request = models.ForeignKey('customer.Design_request', on_delete=models.CASCADE)
    expected_date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    credit = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    credited_date = models.DateField(blank=True, null=True)  # New field to store the credited date
    designer = models.ForeignKey("Designers", on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        try:
            amount_decimal = Decimal(self.amount)  # Ensure it's a Decimal, not a string
            self.credit = amount_decimal * Decimal('0.3')
            self.credited_date = timezone.now().date()  # Set the credited date to current date
        except (InvalidOperation, TypeError):
            self.credit = None  # Fallback in case of invalid data
            self.credited_date = None  # If credit calculation fails, don't set a credited date

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Notification for Design Request {self.design_request.id} - Expected Date: {self.expected_date}, Amount: {self.amount}"





class FreeTemplate(models.Model):
    name= models.CharField(max_length=254)
    image = models.ImageField(upload_to='Designimages/', null=True, blank=True) 


    def __str__(self):
        return self.name
