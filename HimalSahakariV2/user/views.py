from django.shortcuts import get_object_or_404, render,redirect,get_list_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import HttpResponse,HttpResponsePermanentRedirect
from .models import Profile
from django.contrib.auth.models import User
from .forms import UserForm,ProfileForm,CreateUserForm


def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request,username = username,password = password)

        if user is not None:
            login(request,user)
            return redirect('homeapp:index')

        else:
            messages.info(request," युजरनेम वा पासवर्ड मिलेन ")
            return render(request,'user/login.html')
    context = {}

    return render(request,'user/login.html',context)

def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request,('Accounts was created for '+ user))
            return redirect('user:login')
    context = {
        'form':form
    }
    return render(request,'user/register.html',context)
@login_required
def logoutUser(request):
    logout( request )
    messages.success(request,f'{request.user } logged out successfully !')
    return redirect('user:login')

@login_required
def UpdateProfile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST ,instance=request.user)
        profile_form = ProfileForm(request.POST,instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request,('Your Profile is successfully Updated!'))
            return redirect('user:login')
        else:
            messages.error(request,('Please correct the error below!'))
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)

    context = {
        'user_form':user_form,
        'profile_form':profile_form
    }
    return render(request, 'user/profile.html',context)

@login_required
def ViewProfile(request,pk):
    user = get_object_or_404(User,id=pk)
    profile = get_object_or_404(Profile,id=pk)
    context = {
        'user':user,
        'profile':profile,
    }
    return render(request,'user/viewprofile.html',context)

