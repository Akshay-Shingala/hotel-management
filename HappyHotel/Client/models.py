from django.db import models

# Create your models here.
class ClientUser(models.Model):
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    emailId=models.EmailField(max_length=254)
    mobileNumber=models.CharField(max_length=13)
    creatinDate=models.DateField(auto_now_add=True)
    password=models.TextField()
    
    def __str__(self) -> str:
        return self.firstName+" "+self.lastName
    
    
    
    
    
    
    
    
    
    
    