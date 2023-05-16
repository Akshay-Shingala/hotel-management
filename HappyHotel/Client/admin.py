from django.contrib import admin
from . models import ClientUser
class ClientUserAdmin(admin.ModelAdmin):
    list_display = ['firstName', 'lastName','emailId','mobileNumber','password']

admin.site.register(ClientUser,ClientUserAdmin)