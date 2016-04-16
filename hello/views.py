from django.contrib.auth.models import User
from django.contrib import auth

from .models import Link

from .forms import (Linkform,InpurDateForDisplay,RegistrationForm,DateRangeForm,ChangeUsername,ChangeEmail,Dadsmail,LoginForm)
from django.http import (HttpResponseRedirect,HttpResponse)
from django.shortcuts import (render,render_to_response,get_list_or_404,get_object_or_404)
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.core.urlresolvers import reverse

from django.core.mail import (send_mail,BadHeaderError,EmailMessage)

from io import BytesIO,StringIO

import datetime

import csv

from chartit import DataPool,Chart

from .models import Greeting

import requests
import os
# Create your views here.

def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, 'db.html', {'greetings': greetings})

def index(request):
    user=request.user
    return render(request,'hello/base.html',{'user':user,})

def register(request):
    if request.POST:
        form=RegistrationForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']
            email=form.cleaned_data['email']
            user=User.objects.create_user(username=username,password=password,email=email)
            user.save()
            user=auth.authenticate(username=username,password=password)
            auth.login(request,user)
            return HttpResponseRedirect(reverse('homepage',args=(request.user.id,)))
    else:
        form=RegistrationForm()
    return render(request,'hello/registration/register.html',{'form':form,})

def login(request,redirect_field_name='/hello/prehome/'):
    if request.POST:
        form=LoginForm(request.POST)
        if form.is_valid():
            username=request.POST['username']
            password=request.POST['password']
            user=auth.authenticate(username=username,password=password)
            user=get_object_or_404(User,username=username,password=password)
            if user is not None and user.is_active:
                auth.login(request,user)
                return HttpResponseRedirect('/hello/prehome/')
            else:
                return HttpResponseRedirect('/accounts/invalid')
    else:
        form=LoginForm()
        return render(request,'allauth/account/login.html',{'form':form,})

def logout(request):
    request.session.flush()
    auth.logout(request)

def prehome(request):
    return HttpResponseRedirect(reverse('homepage',args=(request.user.id,)))

#@never_cache
def homepage(request,user_id):
    request.session['has_filled_range']=False
    request.session['has_filled_display']=False
    user=request.user
    modeldata=DataPool(
    series=[
    {'options':{'source': user.link_set.all()},'terms':['total','date']}
    ])
    cht=Chart(
    datasource=modeldata,series_options=
    [{'options':{'type':'line','stacking':False},'terms':{'date':['total']}}],
    chart_options=
    {'title':
    {'text':'This Month'},
    'xAxis':{
    'title':{'text':'months'}
    }}
    )
    return render(request,'hello/userprofile/homepage.html',{'user':user,'datechart':cht,})
#    else:
#        return render(request,'hello/userprofile/error.html')

@login_required(redirect_field_name='/hello/add', login_url='/accounts/login/')
def add(request,user_id):
    if request.user.is_active:
        if request.user.is_authenticated():
            user=request.user
            if request.POST:
                form=Linkform(request.POST)
                if form.is_valid():
                    date=form.cleaned_data['date']
                    item=form.cleaned_data['item']
                    price=form.cleaned_data['price']
                    quantity=form.cleaned_data['quantity']
                    description=form.cleaned_data['description']
                    total=quantity*price
                    post=Link(date=date,item=item,price=price,quantity=quantity,description=description,total=total)
                    post=form.save(commit=False)
                    us=User.objects.get(id=user.id)
                    dt=str(date)
                    month=datetime.datetime.strptime(dt,"%Y-%m-%d").date().month
                    us.link_set.create(date=date,item=item,price=price,quantity=quantity,description=description,total=total)
                    us.save()
                    return HttpResponseRedirect(reverse('homepage',args=(request.user.id,)))
            else:
                form=Linkform()
            return render(request,'hello/userprofile/add.html',{'form':form,})
        else:
            return render(request,'hello/userprofile/error.html')

@login_required(redirect_field_name='/hello/log/', login_url='/accounts/login/')
def log(request,user_pk):
    if request.user.is_authenticated():
        user=User.objects.get(id=user_pk)
        if request.user.is_active and request.user.id == user.id:
            data=user.link_set.all().order_by('-date')[:10]
            return render(request,'hello/userprofile/log.html',{'data':data,})
        else:
            return render(request,'hello/userprofile/error.html')
    else:
        return render(request,'hello/userprofile/error.html')

def error(request):
    return render(request,'hello/userprofile/error.html')

def displayform(request,user_pk):
    user=User.objects.get(id=user_pk)
    if request.user.is_active and request.user.id==user.id:
        if request.user.is_authenticated():
            if request.session.get('has_filled_display',False):
                request.session['has_filled_display']=False
                return HttpResponseRedirect(reverse('homepage',args=(request.user.id,)))
            if request.POST:
                form=InpurDateForDisplay(request.POST)
                if form.is_valid():
                    dt=form.cleaned_data['dt']
                    dt=str(dt)
                    date=datetime.datetime.strptime(dt,"%Y-%m-%d").date()
                    #data=get_list_or_404(user.link_set,date=date)
                    data=user.link_set.filter(date=date)
                    grand_total=0
                    for obj in data:
                        grand_total+=obj.total
                    request.session['has_filled_display']=True
                    return render_to_response('hello/userprofile/display.html',{'data':data,'grand_total':grand_total,'user':user,})
            else:
                form=InpurDateForDisplay()
            return render(request,'hello/userprofile/displayform.html',{'form':form,})
    else:
        return render(request,'hello/userprofile/error.html')


def editform(request,user_pk):
    user=User.objects.get(id=user_pk)
    if request.user.id==user.id and request.user.is_active:
        if request.user.is_authenticated():
            if request.POST:
                form=InpurDateForDisplay(request.POST)
                if form.is_valid():
                    dt=form.cleaned_data['dt']
                    dt=str(dt)
                    date=datetime.datetime.strptime(dt,"%Y-%m-%d").date()
                    #data=get_list_or_404(user.link_set,date=date)
                    data=user.link_set.filter(date=date)
                    if data is None:
                        return HttpResponse("You didn't buy any stuff")
                    return render(request,'hello/userprofile/selectedit.html',{'data':data,'user':user,})
            else:
                form=InpurDateForDisplay()
            return render(request,'hello/userprofile/editform.html',{'form':form,})

def edit(request,d_id,user_id):
    user=User.objects.get(id=user_id)
    obj=get_object_or_404(user.link_set,id=d_id)
    if request.user.id==user.id and request.user.is_active:
        if request.user.is_authenticated():
            if request.session.get('has_filled_foredit',False):
                request.session['has_filled_foredit']=False
                return HttpResponseRedirect(reverse('homepage',args=(request.user.id,)))
            if request.POST:
                form=Linkform(request.POST)
                if form.is_valid():
                    date=form.cleaned_data['date']
                    item=form.cleaned_data['item']
                    quantity=form.cleaned_data['quantity']
                    price=form.cleaned_data['price']
                    description=form.cleaned_data['description']
                    obj.date=date
                    obj.item=item
                    obj.quantity=quantity
                    obj.price=price
                    obj.description=description
                    obj.total=price*quantity
                    obj.save()
                    user.save()
                    request.session['has_filled_foredit']=True
                    return render_to_response('hello/userprofile/done.html',{'user':user,})
            else:
                form=Linkform(initial={'date':obj.date,'item':obj.item,'quantity':obj.quantity,'price':obj.price,'description':obj.description,})
            return render(request,'hello/userprofile/foredit.html',{'form':form,'d_id':d_id,'user_id':user_id,})

@never_cache
def deleteform(request,user_id):
    user=User.objects.get(id=user_id)
    if request.user.id==user.id and request.user.is_active:
        if request.user.is_authenticated():
            if request.session.get('is_deleted',False):
                request.session['is_deleted']=False
                form=InpurDateForDisplay()
                return render(request,'hello/userprofile/deleteform.html',{'form':form,})
            if request.POST:
                form=InpurDateForDisplay(request.POST)
                if form.is_valid():
                    dt=form.cleaned_data['dt']
                    dt=str(dt)
                    date=datetime.datetime.strptime(dt,"%Y-%m-%d").date()
                    data=user.link_set.filter(date=date)
                    request.session['is_deleted']=True
                    return render_to_response('hello/userprofile/selectdelete.html',{'data':data,'user':user,})
            else:
                form=InpurDateForDisplay()
            return render(request,'hello/userprofile/deleteform.html',{'form':form,})
    else:
        return render(request,'hello/userprofile/error.html')

def delete(request,d_id,user_id):
    user=User.objects.get(id=user_id)
    obj=user.link_set.get(id=d_id)
    obj.delete()
    user.save()
    return render_to_response('hello/userprofile/done.html')

def fromandto(request,user_pk):
    user=User.objects.get(id=user_pk)
    if request.user.id==user.id and request.user.is_active:
        if request.session.get('has_filled_range',False):
            request.session['has_filled_range']=False
            return HttpResponseRedirect(reverse('homepage',args=(request.user.id,)))
        if request.user.is_authenticated():
            if request.POST:
                form=DateRangeForm(request.POST)
                if form.is_valid():
                    dt_from=form.cleaned_data['dt_from']
                    dt_to=form.cleaned_data['dt_to']
                    dt_from=str(dt_from)
                    dt_to=str(dt_to)
                    date_from=datetime.datetime.strptime(dt_from,"%Y-%m-%d").date()
                    date_to=datetime.datetime.strptime(dt_to,"%Y-%m-%d").date()
                    rangedata=user.link_set.filter(date__gte=date_from,date__lte=date_to).order_by('-date')
                    grand_total=0
                    for obj in rangedata:
                        grand_total+=obj.total
                    request.session['has_filled_range']=True
                    return render_to_response('hello/userprofile/daterange.html',{'rangedata':rangedata,'user':user,'grand_total':grand_total,})
            else:
                form=DateRangeForm()
            return render(request,'hello/userprofile/dateform.html',{'form':form,})
    else:
        return render(request,'hello/userprofile/error.html')

def settings(request,user_pk):
    user=User.objects.get(id=user_pk)
    return render_to_response('hello/userprofile/settings.html',{'user':user,})


def changeuserform(request,user_pk):
    user=User.objects.get(id=user_pk)
    if request.user.id==user.id and request.user.is_active:
        if request.user.is_authenticated():
            if request.POST:
                form=ChangeUsername(request.POST)
                if form.is_valid():
                    curruser=form.cleaned_data['curruser']
                    newuser=form.cleaned_data['newuser']
                    user.username = newuser
                    user.save()
                    return HttpResponseRedirect('/hello/saved')
            else:
                form=ChangeUsername()
            return render(request,'hello/userprofile/changeuserform.html',{'form':form,'user':user,})

def changeemailform(request,user_pk):
    user=User.objects.get(id=user_pk)
    if request.user.id==user.id and request.user.is_active:
        if request.user.is_authenticated():
            if request.POST:
                form=ChangeEmail(request.POST)
                if form.is_valid():
                    oldemail=form.cleaned_data['oldemail']
                    newmail=form.cleaned_data['newmail']
                    if user.email != oldemail:
                        raise forms.ValidationError("Invalid Email address")
                    user.email=newmail
                    user.save()
                    return HttpResponseRedirect('/hello/saved')
            else:
                form=ChangeEmail()
            return render(request,'hello/userprofile/changeemailform.html',{'form':form,'user':user,})
    else:
        render(request,'hello/userprofile/error.html')

def saved(request):
    if request.user.is_authenticated():
        return render(request,'hello/userprofile/saved.html')
    else:
        return render(request,'hello/userprofile/error.html')

def password_change(request,template_name='hello/registration/password_change.html',post_change_redirect='hello/saved/'):
    return render(request,'hello/registration/password_change.html',{'form':form,})


def password_change_done(request,template_name='hello/userprofile/saved.html'):
    if request.user.is_authenticated():
        return render(request,'hello/userprofile/saved.html')

def generatecsv(request,user_id):
    user=User.objects.get(id=user_id)
    object=user.link_set.filter(date__month=datetime.datetime.today().month)
    objectname=''
    objtotal=0
    objectname=str(user.username)+"-"+str(datetime.datetime.today().month)+"/"+str(datetime.datetime.today().year)
    response=HttpResponse(content_type='text/csv')
    response['Content-Disposition']='attachment;filename="{}.csv".format(objectname)'
    buffer=StringIO()
    writer=csv.writer(buffer)
    writer.writerow(['Date','Item','Price','Desription','Quantity','Total'])
    writer.writerow([])
    for obj in object:
        writer.writerow([obj.date,obj.item,obj.price,obj.description,obj.quantity,obj.total])
        objtotal+=obj.total
    writer.writerow([])
    writer.writerow(['Grand Total',objtotal])
    csvs=buffer.getvalue()
    buffer.close()
    response.write(csvs)
    sender=user.email
    if request.user.id==user.id and request.user.is_active:
        if request.user.is_authenticated():
            if request.POST:
                form=Dadsmail(request.POST)
                if form.is_valid():
                    reciever=form.cleaned_data['dadsmail']
                    Emailmsg=EmailMessage('subject','body','ritiksaxena12@gmail.com',[reciever],headers={'Reply-To':'ritiksaxena12@gmail.com'})
                    Emailmsg.attach('{}.csv'.format(objectname),csvs,'text/csv')
                    Emailmsg.send()
                    return render_to_response('hello/emails/mailsent.html',{'user':user,})
            else:
                form=Dadsmail()
            return render(request,'hello/emails/sendmail.html',{'form':form,'user':user,})
    else:
        return render(request,'hello/userprofile/error.html')
