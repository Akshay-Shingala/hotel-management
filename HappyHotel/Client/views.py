from datetime import timedelta
from typing import Any
from django import http
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.views.generic import TemplateView,CreateView,ListView,DetailView
from django.urls import reverse
from django.db.models import Q
from .Form import *
from django.contrib import messages
from django.contrib.auth.hashers import check_password,make_password
from .models import ClientUser
import json
from django.core import serializers
from Rooms.models import *

class indexView(ListView):
    model = hotels
    template_name = 'home.html'
    context_object_name = 'hotels'

    def get_queryset(self):
        form = searchCityHotelForm(self.request.GET)
        queryset = super().get_queryset()

        if form.is_valid():
            name = form.cleaned_data.get('name')
            city = form.cleaned_data.get('city')
            # Apply filters based on form data
            if name:
                print('name', name)
                queryset = queryset.filter(name__icontains=name)
            else:
                print("non name")
            if city:
                print('city', city)
                queryset = queryset.filter(city__name__icontains=city)
            else:
                print("non city")

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        city_list = citys.objects.all()
        hotel_list = hotels.objects.all()
        context['cityList'] = [city.name for city in city_list]
        context['hotelnames'] = [hotel.name for hotel in hotel_list]
        context['form'] = searchCityHotelForm(self.request.GET)
        print("contect call")
        return context

    
def Login(request):
    userName=request.POST.get('userName')
    password=request.POST.get('password')
    try:
        user=ClientUser.objects.get(emailId=userName)
        userpass=user.password
        if check_password(password,userpass):
            request.session['username'] = user.firstName
            request.session['userId'] = user.id
            messages.success(request,"login successful")
            return HttpResponseRedirect(reverse('home'))
        else:
            messages.error(request,"password is incorrect")
            return HttpResponseRedirect(reverse('Login'))
    except ClientUser.DoesNotExist:
        messages.error(request,"User does not exist")
        return HttpResponseRedirect(reverse('Login'))

def Logout(request):
    request.session.pop('username')
    return HttpResponseRedirect(reverse('home'))

def ragistrations(request):
    if request.method == "POST":
        form =RagistrationForm(request.POST)
        if form.is_valid():
            formSave=form.save(commit=False)
            formSave.password =make_password(form.cleaned_data["password"])
            formSave.save()
            messages.success(request,"Ragister successfully")
            return HttpResponseRedirect(reverse("home"))
        else:
            messages.error(request,form.errors)
    formR=RagistrationForm()
    context={'form': formR}
    return TemplateResponse(request,"register.html",context)


class CategoryList(TemplateView):
    model = roomCategorys
    template_name = "roomCategory.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        my_kwarg = kwargs.get('id')
        self.request.session['hotel_id']=my_kwarg
        categoryList=hotels.objects.get(id=my_kwarg)
        context['categoryList'] =  categoryList.roomCategory.all()   
        print(categoryList.roomCategory.all())
        return context
    
class CategoryList(TemplateView):
    model = roomCategorys
    template_name = "roomCategory.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        my_kwarg = kwargs.get('id')
        self.request.session['hotel_id']=my_kwarg
        categoryList=hotels.objects.get(id=my_kwarg)
        context['categoryList'] =  categoryList.roomCategory.all()   
        print(categoryList.roomCategory.all())
        return context

class RoomslistView(ListView):
    model=Bookings
    template_name='RoomsList.html'
    def get_queryset(self):
        form = checkInCheckOutForm(self.request.GET)
        queryset = super().get_queryset()

        if form.is_valid():
            checkInDate = form.cleaned_data.get('checkInDate')
            checkOutDate = form.cleaned_data.get('checkOutDate')
            # Apply filters based on form data
            print('name', checkInDate)
            queryset = queryset.filter(Q(checkInTime__date__lte=checkInDate, checkOutTime__date__gte=checkInDate) |
                                            Q(checkInTime__date__lte=checkOutDate, checkOutTime__date__gte=checkOutDate))['id']
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(kwargs.keys())
        categoryId=self.request.GET.get('id')
        self.request.session['categoryId']=categoryId
        context['form']=checkInCheckOutForm(self.request.GET)
        context['roomList'] = rooms.objects.filter(hotelId=self.request.session['hotel_id'],roomCategory=categoryId)
        print(categoryId)
        print(self.request.session['hotel_id'])
        print(context['roomList'])
        return context    
class RoomsList(TemplateView):
    template_name='RoomsList.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categoryId=kwargs.get('category')
        print(self.request.session['hotel_id'])
        self.request.session['categoryId']=categoryId
        print(categoryId)
        checkInDate=datetime.date.today() if kwargs.get('checkInDate') == None else kwargs.get('checkInDate')
        checkOutDate =checkInDate + timedelta(days=1)if kwargs.get('checkOutdate') == None else kwargs.get('checkoutDate')
        roomList = rooms.objects.filter(hotelId=self.request.session['hotel_id'],roomCategory=categoryId)
        print(checkInDate)
        print(checkOutDate)
        
        bookingList=Bookings.objects.filter(Q(checkInTime__date__lte=checkInDate, checkOutTime__date__gte=checkInDate) |
                                            Q(checkInTime__date__lte=checkOutDate, checkOutTime__date__gte=checkOutDate))
        context['checkInDate'] = checkInDate
        context['checkOutDate'] = checkOutDate
        context['roomList']=roomList
        context['category']=categoryId
        context['bookingList']=[x.room.id for x in bookingList] 
        return context
def filterRoomsByDate(request):
    hotelId=request.session['hotel_id']
    categoryId=request.session['categoryId']
    checkInDate=request.GET.get('checkInDate')
    checkOutDate=request.GET.get('checkOutDate')
    bookingsList=Bookings.objects.filter(Q(checkInTime__date__lte=checkInDate, checkOutTime__date__gte=checkInDate) |
                                            Q(checkInTime__date__lte=checkOutDate, checkOutTime__date__gte=checkOutDate))
    roomList = rooms.objects.filter(hotelId=hotelId,roomCategory=categoryId)
    hotel=hotels.objects.get(id=hotelId)
    category =roomCategorys.objects.get(id=categoryId)
    room_data = serializers.serialize('json', roomList)
    # booklist=
    return JsonResponse({'status': room_data,'hotel':hotel.name, 'category': category.name,'bookingList':[x.room.id for x in bookingsList]})


def bookRoom(request):
    roomId=request.POST.get('room')
    print("***********")
    csrf_token=request.POST.get('')
    checkInDate=request.POST.get('checkInDate')
    checkOutDate=request.POST.get('checkOutDate')
    user=ClientUser.objects.get(id=request.session['userId'])
    room=rooms.objects.get(id=roomId)
    Bookings.objects.create(userId=user,room=room,checkInTime=checkInDate,checkOutTime=checkOutDate)
    return HttpResponseRedirect(reverse('home'))
class roomDetails(DetailView):
    model=rooms
    template_name='booking.html'