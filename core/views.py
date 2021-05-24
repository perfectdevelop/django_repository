from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from .models import UserType, User, DonatorInfo, Order
from .forms import DonatorInfoForm


@login_required(login_url="/login")
def index(request):
    context = {}
    user = UserType.objects.get(user=request.user)
    if user.typeName == 'donator':
        if(request.method == 'POST'):
            donator_info = DonatorInfoForm(request.POST)
            print(donator_info.is_valid())
            if donator_info.is_valid():
                donators = donator_info.save()
                donators.donator = user
                donators.save(0)
                donatorinfo = DonatorInfo.objects.filter(donator=user).exists()
                # donator_info.save()
                return render(request, 'index.html', {"donatorinfo": donatorinfo})
        donatorinfo = DonatorInfo.objects.filter(donator=user).exists()
        context['donatorinfo'] = donatorinfo
        if donatorinfo:
            donators = DonatorInfo.objects.filter(donator=user)[0]
            context['donator'] = donators
        return render(request, 'index.html', context)

    else:
        all_donator = DonatorInfo.objects.all()
        for donate in all_donator:
            order = donate.order_set.all()
            if(order.count() > 0):
                donate.order = order[0]
            else:
                donate.order = False
        context['all_donator'] = all_donator
        return render(request, 'patientIndex.html', context)


def update_donator(request):
    if request.method == 'POST':
        id = request.POST['id']
        blood_group = request.POST['blood_group']
        information = request.POST['information']
        donate_amount = request.POST['donate_amount']
        donator_update = DonatorInfo.objects.get(id=id)
        donator_update.information = information
        donator_update.donate_amount = donate_amount
        donator_update.blood_group = blood_group
        donator_update.save()
        return redirect('/')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            if request.GET.get('next', None):
                return HttpResponseRedirect(request.GET['next'])
            return redirect('/')
        else:
            return render(request, 'login.html')
    return render(request, 'login.html')


def register(request):
    if request.method == 'POST':
        name = request.POST['name']
        typeName = request.POST['userType']
        username = request.POST['emailOrUsername']
        # mobile = request.POST['Mobile']
        password = request.POST['password']
        # address = request.POST['address']
        user = User.objects.create_user(
            username=username, password=password, first_name=name)
        print(user)
        assignUserType = UserType(user=user, typeName=typeName)
        assignUserType.save()
        return redirect('/login')

    return render(request, 'register.html')


def delete_donator(request, id):
    # id = request.POST['id']
    donator_update = DonatorInfo.objects.get(id=id)
    donator_update.delete()
    # print(donator_update)
    # print("donator_update")
    return redirect('/')

def logout_user(request):
    logout(request)
    return redirect('/login')


def order_create(request, pat, don):
    donar = DonatorInfo.objects.get(id=don)
    patient = User.objects.get(id=pat)
    order_obj = Order(donator=donar, patient=patient)
    order_obj.save()
    return redirect('/')

def get_json(request):
    A = 0
    B = 0
    AB = 0
    O = 0
    for var in DonatorInfo.objects.all() :
        if var.blood_group == 'A' :
            A += 1
        if var.blood_group == 'B' :
            B += 1
        if var.blood_group == 'AB' :
            AB += 1
        if var.blood_group == 'O' :
            O += 1
    return JsonResponse({'A':A,'B':B,'AB':AB,'O':O}, safe=False)
