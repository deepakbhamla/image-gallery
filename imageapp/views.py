from .models import Gallery, Tag
from .forms import GalleryForm
from django.contrib import messages
from PIL import Image
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import random
from django.shortcuts import render, redirect ,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login , logout
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

# Create your views here.
def Home(request):
    img = Gallery.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(img, 8)
    try:
        data = paginator.page(page)
    except PageNotAnInteger:
        data = paginator.page(1)
    except EmptyPage:
        data = paginator.page(paginator.num_pages)

    navigation = Tag.objects.all()
    
    ctx = {'data' : data, 'navigation' : navigation}
    return render(request,'imageapp/home/home.html', ctx)


def UploadImage(request):
        if request.method == 'POST':
            form = GalleryForm(request.POST, request.FILES)
            if form.is_valid():
                for img in request.FILES.getlist('image'):    
                    tag = form.cleaned_data.get("tags")
                    tag_list = []
                    for data in tag:
                        if data in Tag.objects.all():
                          tag_list.append(data)

                    ins = Gallery.objects.create(image=img)
                    ins.tags.set(tag_list)
                        
                messages.success(request, 'images upload successfuly')
                return redirect('upload-image')
            else :    
                messages.success(request, 'images not upload please choose tag ')
                return redirect('upload-image')

        form = GalleryForm()
        context = {'form': form}
        return render(request, 'imageapp/upload-image/upload.html', context)





def TagCategory(request,single_slug):
    data = Gallery.objects.filter(tags__slug__contains=single_slug)
    navigation = Tag.objects.all()
    ctx = {'data' : data, 'navigation' : navigation}

    return render(request, 'imageapp/home/home.html', ctx)    



def EditImage(request,pk):
    img = get_object_or_404(Gallery, pk=pk)
    ctx = {'img' : img}

    return render(request, 'imageapp/edit-image/edit.html', ctx)    

def RotateAnti(request,pk):
    img = get_object_or_404(Gallery, pk=pk)
    path = img.image
    Original_Image = Image.open(path)
    rotated_image = Original_Image.rotate(90, expand= True)
    rotated_image.save(img.image.file.name, overwrite=False)
    messages.success(request, 'images rotate 90 Degree anti-clockwise')
    

    ctx = {'img' : img}
    return redirect(f'/edit/{pk}',ctx)
 
def RotateClock(request,pk):
    img = get_object_or_404(Gallery, pk=pk)
    path = img.image
    Original_Image = Image.open(path)
    rotated_image = Original_Image.rotate(-90, expand= True)
    print("clockwise rotate ::::::",rotated_image)
    rotated_image.save(img.image.file.name, overwrite=False)
    messages.success(request, 'images rotate 90 Degree clockwiswe')
    

    ctx = {'img' : img}
    return redirect(f'/edit/{pk}',ctx)



def SignupView(request):
    if request.method == 'POST':
        print("user adding started")
        username = request.POST['username']
        firstname = request.POST['firstname']
        email = request.POST['email']

        if len(username) > 12:
            messages.success(request, 'username charector limit exceed')
            return redirect(request.META.get('HTTP_REFERER'))

        print(":::::::::::::::::",email)  
        otp = random.randint(100,9999)
        print(":::::::::::::::::",otp)
        context= {
            'firstname':firstname,
        }
        request.session['username'] = username
        request.session['email'] = email
        request.session['firstname'] = firstname
        request.session['otp'] = otp



        return render(request,'imageapp/account/account.html',context)
    else:
        return HttpResponse("not created")    

def AuthView(request):
    if request.method == 'POST':
        username = request.session['username']
        firstname = request.session['firstname']
        email = request.session['email']
        otp = request.session['otp']

        otp1 = request.POST['otp1']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        context= {
            'firstname':firstname,
        }


        print(otp)
        print(otp1)
        if int(otp) != int(otp1):
            messages.success(request, 'OTP Not Valid')
            return render(request,'imageapp/account/account.html',context)

        if password1 != password2:
            messages.success(request, 'Password Didn`t Match')
            return render(request,'imageapp/account/account.html',context)

        if len(username) > 12:
            messages.success(request, 'username charector limit exceed Please Try Again!')
            return render(request,'imageapp/account/account.html',context)

        new_user = User.objects.create_user(username,email,password1)
        new_user.first_name =firstname
        new_user.save()
        print("user added successfully")  
        user = authenticate(username = username, password = password1)   
        if user is not None:
            login(request, user)
            messages.success(request, f'{firstname} Welcome To million of Images Gallery ') 
            return redirect('/')
    else:
        
        return redirect(request.META.get('HTTP_REFERER'))

def LoginView(request):
    if request.method == 'POST':
        login_username = request.POST['username']
        login_password = request.POST['password']

        user = authenticate(username = login_username, password = login_password)  
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome Back {login_username} ')
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            messages.success(request, 'Username and password are not correct! try again.')
            return redirect(request.META.get('HTTP_REFERER'))
    return HttpResponse("not found")

def LogoutView(request):
            logout(request)
            messages.success(request, f'You Are Successfully Log Out')
            return redirect('/')
