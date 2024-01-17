from django.shortcuts import render
from django.http import HttpResponseForbidden,HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login, logout
from .models import CustomUser,Product,Category,Personal
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags





# Create your views here.
def home(request):
    products = Product.objects.all()
    
    is_superuser = request.user.is_superuser
    is_authenticated = request.user.is_authenticated
    context = {
        'is_authenticated': is_authenticated,
        'is_superuser': is_superuser,      
    }
    return render(request, "home.html", {'products': products, **context})


def register(request): 
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect("register")
        elif password == confirm_password:
            CustomUser.objects.create_user(username=username, password=password)
            return redirect('login')
        else:
            error_message = "Passwords do not match."
            return render(request, 'register.html', {'username': username, 'error_message': error_message})

    return render(request, 'register.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
       


        user = authenticate(request, username=username, password=password)
        print(user)
        if user is None:
            # return render(request, 'login.html') 
            return render(request, 'login.html', {'error_message': 'Invalid login credentials!'})
        else:
            login(request, user)
            return redirect('home')
    return render(request, 'login.html')


def user_logout(request):
    logout(request)
    return redirect('home')


def productadd(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            title = request.POST.get('title')
            description = request.POST.get('description')
            price = request.POST.get('price')
            categories = request.POST.getlist('categories')
            image = request.FILES.get('image')  # Get the uploaded image file
    
            # Create a new Product instance using the extracted data
            new_product = Product.objects.create(
                title=title,
                description=description,
                price=price,
                image=image,
                # Assign values to other fields here
            )
    
            # Assign categories to the new product
            for category_id in categories:
                category = Category.objects.get(id=category_id)
                new_product.categories.add(category)
    
            # Redirect to a page displaying the newly created product
            return redirect('product_detail', pk=new_product.pk)  # Assuming product_detail is the view for product details
    
        categories = Category.objects.all()  # Query all categories from your database
        context = {'categories': categories}
        return render(request, "productadd.html", context)
    else:
            # The user is authenticated but not a superuser
            return HttpResponseForbidden("You don't have permission to access this page.")


def categoryadd(request):
        categories = Category.objects.all() 
        if request.method == 'POST':
          name = request.POST.get('name')
          Category.objects.create(name = name)
        return render(request,"categoryadd.html", {'categories': categories})

def delete_category(request, category_id):
    category = Category.objects.get(pk=category_id)
    
    if request.method == 'POST':
        category.delete()
        return redirect('categoryadd')

    return render(request, 'delete_category.html', {'category': category})

def edit_category(request, category_id):
    category = Category.objects.get(pk=category_id)

    if request.method == 'POST':
        # Update category fields based on POST data
        category.name = request.POST.get('name')
        category.save()
        return redirect('categoryadd')

    return render(request, 'edit_category.html', {'category': category})

def product_view(request):
    products = Product.objects.all()
    return render(request,"product_view.html",{'products': products})

def check_admin(user):
    if not user.is_superuser:
        return False
    return True

# @user_passes_test(check_admin, login_url="user_detail/pk")
def product_detail(request, pk):
   if  check_admin(request.user): 
      product = get_object_or_404(Product, pk=pk)
  
     
      return render(request, 'product_detail.html', {'product': product})
   return redirect('user_detail', pk=pk)

def user_detail(request, pk):
   
    product = get_object_or_404(Product, pk=pk)

   
    return render(request, 'user_detail.html', {'product': product})

def edit(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    if request.method == 'POST':
        product.title = request.POST.get('title')
        product.description = request.POST.get('description')
        product.price = request.POST.get('price')
        new_image = request.FILES.get('image')

        
        categories = request.POST.getlist('categories')

        
        if new_image:
            product.image = new_image

        product.save()

        return redirect('product_view')

    categories = Category.objects.all()
    return render(request, "edit.html", {'product': product, 'categories': categories})



@login_required
def update_profile(request):
    try:
        profiles = Personal.objects.get(user=request.user)
    except Personal.DoesNotExist:
        profiles = Personal(user=request.user)
    
    if request.method == 'POST':
        # Get the current user
        
        last_name = request.POST.get('last_name')
        first_name = request.POST.get('first_name')
        new_email = request.POST.get('email') 
        profile = request.FILES.get('profile') 

        if Personal.objects.exclude(user=request.user).filter(email=new_email).exists():
            messages.error(request, 'This email is already in use. Please choose a different one.')
            return render(request, 'update_profile.html', {'profiles': profiles})
        
        profiles.last_name=last_name
        profiles.first_name=first_name
        profiles.email=new_email
        if profile:
            profiles.profile = profile
        profiles.save()
        subject = "Profile Update Confirmation"
        from_email = "lekshmi.anilkumar06@gamil.com"
        to_email = [profiles.email]
        print(profiles.email)
        html_content = render_to_string("email.html", {'profiles': profiles})
        text_content = strip_tags(html_content)
        msg = EmailMultiAlternatives(subject, text_content, from_email, to_email)
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        messages.success(request, 'Profile updated successfully! and an email has been send to you ')
        return redirect('profile')
        

        

    return render(request, "update_profile.html", {'profiles': profiles})

def email(request):
    profiles = Personal(user=request.user)
    return render(request, "email.html",  {'profiles': profiles})

@login_required
def profile(request):
    profiles, created = Personal.objects.get_or_create(user=request.user)
    
    if not profiles.last_name or not profiles.first_name or not profiles.email:
        return redirect('update_profile')
    return render(request,"profile.html",{'profiles': profiles})

def delete_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        product.delete()
        return redirect('product_view') 


    