from datetime import timedelta
from typing import Any
from django import http
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.views.generic import TemplateView,CreateView,ListView
from django.urls import reverse
from django.db.models import Q
from .Form import RagistrationForm
from django.contrib import messages
from django.contrib.auth.hashers import check_password,make_password
from .models import ClientUser
from Rooms.models import *
class indexView(TemplateView):
    template_name="home.html"
    city=None
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cityList=citys.objects.all()
        city = kwargs.get('citys')
    
        if city is not None:
            hotelsList=hotels.objects.filter(city__name=city)
        else:
            hotelsList=hotels.objects.all()
        
        context={'cityList':cityList, 'hotelsList':hotelsList}
        return context    
def Login(request):
    userName=request.POST.get('userName')
    password=request.POST.get('password')
    try:
        user=ClientUser.objects.get(emailId=userName)
        userpass=user.password
        if check_password(password,userpass):
            request.session['username'] = user.firstName
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
    
class RoomsList(TemplateView):
    template_name='RoomsList.html'
    def put(self, request):
        checkInDate=self.request.get('checkInDate')
        checkOutDate=self.request.get('checkOutDate')
        return super().get_context_data(request,{'checkInDate':checkInDate, 'checkOutDate':checkOutDate})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categoryId=kwargs.get('category')
        print(self.request.session['hotel_id'])
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

# def bookRoom(request):
#     if request.method == 'POST':
        