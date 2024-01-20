from django.db import models

class Car(models.Model):
    url = models.URLField()
    title = models.CharField(max_length=255)
    price_usd = models.DecimalField(max_digits=10, decimal_places=2)
    odometer = models.IntegerField()
    username = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20) 
    image_url = models.URLField()
    images_count = models.IntegerField()
    car_number = models.CharField(max_length=20)  
    car_vin = models.CharField(max_length=17)  
    datetime_found = models.DateTimeField(auto_now_add=True)