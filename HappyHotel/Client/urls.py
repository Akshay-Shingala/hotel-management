from django.urls import path
from . views import *
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('',indexView.as_view(),name="home"),
    # path('hotels/<str:city>',indexviewFilter.as_view(),{'city':None},name="homefilterbycity"),
    path('happy hotel/Login',Login,name="Login"),
    path('happy hotel/Logout',Logout,name="Logout"),
    path('happy hotel/Hotel/<str:id>',CategoryList.as_view(),name="CategoryList"),
    path('happy hotel/ragistrations',ragistrations,name="ragistrations"),
    path('happy hotel/Rooms/<str:id>',RoomslistView.as_view(),name="RoomsList"),
    path('happy hotel/filter Rooms by date',filterRoomsByDate,name="filterRoomsByDate"),
    path('happy hotel/room detail/<pk>',roomDetails.as_view(),name="bookdetails"),
    path('happy hotel/Book Room',bookRoom,name="BookRoom"),
    # path('happy hotel\Hotels',)
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
