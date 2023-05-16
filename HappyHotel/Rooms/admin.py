from django.contrib import admin
from .models import *

class hotelAdmin(admin.ModelAdmin):
    list_display=['name','state','city','roomCategoryFun','contectNumber']
    
    @admin.display(empty_value="???")
    def roomCategoryFun(self,obj):
        return " ".join([x.name+" " for x in obj.roomCategory.all()])
        
admin.site.register(hotels,hotelAdmin)

class roomCategoryAdmin(admin.ModelAdmin):
    list_display=['name']
admin.site.register(roomCategorys,roomCategoryAdmin)

class stateAdmin(admin.ModelAdmin):
    list_display=['name']
admin.site.register(states,stateAdmin)

class cityAdmin(admin.ModelAdmin):
    list_display=['name']
admin.site.register(citys,cityAdmin)

class BookingAdmin(admin.ModelAdmin):
    list_display=['userId','room','checkInTime','checkOutTime']

admin.site.register(Bookings,BookingAdmin)

class roomsAdmin(admin.ModelAdmin):
    list_display=['hotelId','roomCategory','roomNumber','description','pricePerDay']
admin.site.register(rooms,roomsAdmin)

class RoomImageAdmin(admin.ModelAdmin):
    list_display=['roomId','roomImages']
admin.site.register(roomImages,RoomImageAdmin)