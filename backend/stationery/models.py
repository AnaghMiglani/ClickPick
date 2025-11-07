from django.db import models
from . import utils
from django.utils.html import mark_safe
from authentication.models import User


# Model for all items in the stationery
class Items(models.Model):

    item = models.CharField(max_length=25)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    in_stock = models.BooleanField(default=True)
    display_image = models.ImageField(upload_to=utils.upload_display_image, null=True, blank=True)

    def __str__(self):
        return self.item

    def image_preview(self):
        if self.display_image:
            return mark_safe(f'<img src = "{self.display_image.url}" width = "100"/>')
        return "No image"

    class Meta:
        db_table = 'stationery_items'  
        verbose_name_plural = "All Items"



# Model for active orders
class ActiveOrders(models.Model):

    order_id = models.AutoField(primary_key=True)   #auto generated auto incrementing

    user = models.ForeignKey(User, max_length=50, on_delete=models.SET_NULL, null=True, db_column='user')

    item = models.ForeignKey(Items, max_length=25, on_delete=models.SET_NULL, null=True, db_column='item')
    quantity = models.PositiveIntegerField()
    cost = models.DecimalField(max_digits=6, decimal_places=2)
    custom_message = models.TextField(blank=True)
    order_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.order_id)

    class Meta:
        db_table = 'stationery_active_orders'  
        verbose_name_plural = "Active Orders"

# Model for completed (past) orders
class PastOrders(models.Model):

    order_id = models.CharField(max_length=7, unique=True, db_index=True)  

    user = models.ForeignKey(User, max_length=50, on_delete=models.SET_NULL, null=True, db_column='user') 

    item = models.ForeignKey(Items, max_length=25, on_delete=models.SET_NULL, null=True, db_column='item')
    quantity = models.PositiveIntegerField()
    cost = models.DecimalField(max_digits=6, decimal_places=2)
    custom_message = models.TextField(blank=True)
    order_time = models.DateTimeField()

    def __str__(self):
        return self.order_id

    class Meta:
        db_table = 'stationery_past_orders'  
        verbose_name_plural = "Past Orders"


# Model for active printouts
class ActivePrintOuts(models.Model):
    
    order_id = models.AutoField(primary_key=True)
    
    user = models.ForeignKey(User, max_length=50, on_delete=models.SET_NULL, null=True, db_column='user')
    
    cost = models.DecimalField(max_digits=6, decimal_places=2)
    custom_message = models.TextField(blank=True)
    order_time = models.DateTimeField(auto_now_add=True)

    file = models.FileField(upload_to=utils.printout_rename)

    def __str__(self):
        return str(self.order_id)

    class Meta:
        db_table = 'stationery_active_printouts'  
        verbose_name_plural = "Active Print-Outs"
        
# Model for completed (past) printouts
class PastPrintOuts(models.Model):

    order_id = models.CharField(max_length=7, unique=True, db_index=True)

    user = models.ForeignKey(User, max_length=50, on_delete=models.SET_NULL, null=True, db_column='user')   

    cost = models.DecimalField(max_digits=6, decimal_places=2)
    custom_message = models.TextField(blank=True)
    order_time = models.DateTimeField()

    file = models.FileField(upload_to=utils.printout_rename)
    
    def __str__(self):
        return self.order_id

    class Meta:
        db_table = 'stationery_past_printouts'  
        verbose_name_plural = "Past Print-Outs"

class PrintoutFile(models.Model):
    """
    Allows multiple files to be attached to a single printout order.
    Links to either active or past printout.
    """
    printout_active = models.ForeignKey(
        ActivePrintOuts, 
        related_name='files', 
        on_delete=models.CASCADE,
        null=True, 
        blank=True
    )
    printout_past = models.ForeignKey(
        PastPrintOuts, 
        related_name='files', 
        on_delete=models.CASCADE,
        null=True, 
        blank=True
    )
    file = models.FileField(upload_to=utils.printout_file_rename)
    file_name = models.CharField(max_length=255, blank=True)  # Original filename
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file_size = models.BigIntegerField(default=0)  # Size in bytes
    
    # Printing specifications for this specific file
    coloured_pages = models.CharField(max_length=20, blank=True)
    black_and_white_pages = models.CharField(max_length=20, blank=True)
    print_on_one_side = models.BooleanField(null=True, blank=True)
    
    def __str__(self):
        if self.printout_active:
            return f"File for Active Printout {self.printout_active.order_id}"
        elif self.printout_past:
            return f"File for Past Printout {self.printout_past.order_id}"
        return f"PrintoutFile {self.id}"
    
    class Meta:
        db_table = 'stationery_printout_files'
        verbose_name_plural = "Printout Files"

# For temporarily storing the generated first_page 
class TempFileStorage(models.Model):
    file = models.FileField(upload_to=utils.temp_file_rename)