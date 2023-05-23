from datetime import timedelta
from typing import Any
from django import http
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.views.generic import TemplateView,CreateView,ListView,DetailView,DeleteView
from django.urls import reverse, reverse_lazy
from django.db.models import Q,Sum
from .Form import *
from django.contrib import messages
from django.contrib.auth.hashers import check_password,make_password
from .models import ClientUser
from django.template.response import TemplateResponse
from django.core import serializers
from Rooms.models import *
from django.utils import timezone
import datetime
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
                queryset = queryset.filter(name__icontains=name)
            if city:
                
                queryset = queryset.filter(city__name__icontains=city)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        city_list = citys.objects.all()
        hotel_list = hotels.objects.all()
        context['cityList'] = [city.name for city in city_list]
        context['hotelnames'] = [hotel.name for hotel in hotel_list]
        context['form'] = searchCityHotelForm(self.request.GET)

        return context

    
def Login(request):
    userName=request.POST.get('userName')
    password=request.POST.get('password')
    try:
        user=ClientUser.objects.get(emailId=userName)
        userpass=user.password
        if check_password(password,userpass):
            request.session['username'] = user.firstName
            request.session['userId']=user.id
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
        
        return context

class RoomslistView(ListView):
    model=Bookings
    template_name='RoomsList.html'
    def get_queryset(self):
        form = checkInCheckOutForm(self.request.GET)
        queryset = super().get_queryset()
        today=datetime.datetime.now() 
        checkInDate=datetime.datetime.now()
        checkOutDate=today + datetime.timedelta(days=1)
        if form.is_valid():
            checkInDate = form.cleaned_data.get('checkInDate')
            checkOutDate = form.cleaned_data.get('checkOutDate')
            # Apply filters based on form data
        print("checkInDate",checkInDate)
        print("checkOutDate",checkOutDate)
        queryset = Bookings.objects.filter(Q(checkInTime__range=[checkInDate, checkOutDate],checkOutStatus=False) |Q( checkOutTime__range=[checkInDate, checkOutDate],checkOutStatus=False))
        print(queryset)
        a=checkInDate
        b=checkOutDate
        delta = b - a
        rooms=[x.room for x in queryset]
        days =delta.days
        queryset={'rooms':rooms,'days':days}
        return queryset
        

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categoryId=self.kwargs.get('id')
        self.request.session['categoryId']=categoryId
        today=datetime.datetime.now()
        print(today,"today") 
        context['form']=checkInCheckOutForm(self.request.GET)
        context['roomList'] = rooms.objects.filter(hotelId=self.request.session['hotel_id'],roomCategory=categoryId)
        
        return context    
def myCheckOut(request):
    myBookingsId=request.POST.get('bookingId')
    now=timezone.now()
    object =Bookings.objects.get(id=myBookingsId,userId__id=request.session['userId'])
    if object.checkInTime < now and object.checkOutTime > now and not object.checkOutStatus:
        object.checkOutStatus = True
        object.save()
    return HttpResponseRedirect(reverse('myBookings'))     
   
class feedbackView(TemplateView):
    template_name="feedback.html"
    def post(self, request, *args, **kwargs):
        hotel=self.request.POST.get('hotelId')
        ls=[self.request.POST.get('star1',False),self.request.POST.get('star2',False),self.request.POST.get('star3',False),self.request.POST.get('star4',False),self.request.POST.get('star5',False)]
        msg=self.request.POST.get('msg','')
        user=ClientUser.objects.get(id=self.request.session['userId'])
        hotel=hotels.objects.get(id=hotel)
        feedback.objects.update_or_create(user=user,hotel=hotel,defaults={"rating": ls.count('on'),'msg':msg})
        allFeedbacks=feedback.objects.filter(hotel=hotel)
        totalStars=allFeedbacks.aggregate(Sum('rating'))
        totalStars=totalStars['rating__sum']
        numberOfFeedback=allFeedbacks.count()
        print("********************************")
        print(totalStars,numberOfFeedback)
        print("********************************")
        rating=round((totalStars/(numberOfFeedback*5))*5)
        hotel.reating=rating
        hotel.save()
        return HttpResponseRedirect('/happy hotel/myBookings')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(self.kwargs['pk'])
        context['hotelId'] =self.kwargs['pk']
        return context
    
    
class myBookings(TemplateView):
    template_name="myBookings.html"
    def post(self, request, *args, **kwargs):
        Bookings.objects.filter(id=self.request.POST.get('bookingId')).update(bookingStatus="cancelled",checkOutStatus=True)
        return HttpResponseRedirect(reverse('myBookings'))
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["myBookings"] =Bookings.objects.filter(userId__id=self.request.session['userId'])
        now=datetime.datetime.now().astimezone()
        print(datetime.datetime.now().astimezone(),now)
        for booking in context["myBookings"]:
            if booking.checkInTime < now and booking.checkOutTime > now and not booking.checkOutStatus:
                print(True,"***",booking.checkInTime, "<", now ,"and", booking.checkOutTime ,">", now ,"and not", booking.checkOutStatus)
                booking.allowCheckOut = True
            else:
                print(False,"***",booking.checkInTime, "<", now ,"and", booking.checkOutTime ,">", now ,"and not", booking.checkOutStatus)
        return context

def bookRoom(request):
    roomId=request.POST.get('room')
    csrf_token=request.POST.get('')
    checkInDate=request.POST.get('checkInDate')
    check_in_datetime = datetime.datetime.strptime(checkInDate, "%Y-%m-%dT%H:%M")
    checkOutDate=request.POST.get('checkOutDate')
    check_Out_datetime = datetime.datetime.strptime(checkOutDate, "%Y-%m-%dT%H:%M")
    user=ClientUser.objects.get(id=request.session['userId'])
    room=rooms.objects.get(id=roomId)
    book=Bookings.objects.filter(Q(room=room), Q(checkInTime__date__range=[check_in_datetime, check_Out_datetime,],checkOutStatus=False),Q(checkOutTime__date__range=[check_in_datetime, check_Out_datetime],checkOutStatus=False))
    if len(book) == 0:
        messages.success(request,"Room booked successfully")
        try:
            Bookings.objects.create(userId=user,room=room,checkInTime=checkInDate,checkOutTime=checkOutDate)
        except Exception as e:
            print("Error creating",e)
    else:
        messages.error(request,"Room already for this date")
    return HttpResponseRedirect(reverse('home'))
class roomDetails(DetailView):
    model=rooms
    template_name='booking.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] =checkInCheckOutForm()
        return context
def error404(request,exception):
    return render(request,'404.html', status=404)
