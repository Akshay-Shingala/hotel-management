import datetime
from django.db import models
from django.forms import ValidationError
from Client.models import *
from django.core.validators import MaxValueValidator,MinValueValidator
from .validator import *
class states(models.Model):
    name=models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class citys(models.Model):
    state=models.ForeignKey(states, on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class roomCategorys(models.Model):
    imagepic = models.ImageField(upload_to="category_images")
    name=models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class hotels(models.Model):
    name=models.CharField(max_length=100)
    state=models.ForeignKey(states, on_delete=models.CASCADE)
    city=models.ForeignKey(citys, on_delete=models.CASCADE)
    roomCategory=models.ManyToManyField(roomCategorys)
    contectNumber=models.CharField(max_length=15,validators=[validate_mobile])
    hotelImage=models.ImageField(upload_to="Hotel_pic")
    reating=models.IntegerField(default=1,validators=[ MinValueValidator(limit_value=1,message="minimum rating value 1"),MaxValueValidator(limit_value=5,message="maximum rating value 5")])
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = 'hotel'
        verbose_name_plural = 'hotels'

class rooms(models.Model):
    hotelId = models.ForeignKey(hotels,on_delete=models.CASCADE)
    roomCategory=models.ForeignKey(roomCategorys, on_delete=models.CASCADE)
    roomNumber = models.IntegerField()
    description = models.TextField()
    pricePerDay= models.IntegerField(validators=[numberValidation])
    roomImage=models.ImageField(upload_to="roomImage")
    def __str__(self) -> str:
        return self.hotelId.name + " "+ str(self.roomNumber)
bookingChoice = (('Running', 'Running'), ('Pending', 'pending'), ('cancelled', 'cancelled'),('expired', 'expired'))
class Bookings(models.Model):
    userId=models.ForeignKey(ClientUser, verbose_name=("user Booked"), on_delete=models.CASCADE)
    room=models.ForeignKey(rooms, on_delete=models.CASCADE)
    bookingStatus=models.CharField(max_length=100,choices=bookingChoice,default="Pending")
    checkInTime=models.DateTimeField(validators=[checkIndateValidation])
    checkOutTime=models.DateTimeField()
    checkOutStatus=models.BooleanField(default=False)
    # def clean(self, *args, **kwargs):
    #     # run the base validation
    #     super(Bookings, self).clean(*args, **kwargs)

    #     # Don't allow dates older than now.
    #     if self.checkInTime < datetime.datetime.now():
    #         raise ValidationError('Start time must be later than now.')
    
class roomImages(models.Model):
    roomId=models.ForeignKey(rooms, verbose_name=("hotel room"), on_delete=models.CASCADE)
    roomImages=models.ImageField(upload_to="Rooms")

class feedback(models.Model):
    user=models.ForeignKey(ClientUser, on_delete=models.CASCADE)
    hotel=models.ForeignKey(hotels, on_delete=models.CASCADE)
    rating=models.IntegerField(default=1)
    msg=models.TextField(blank=True)