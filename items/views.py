from django.shortcuts import render
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import CustomUser,Product,Category
from django.contrib import messages


# Create your views here.
def home(request):
    return render(request, "home.html")


def register(request): 
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        if CustomUser.objects.filter(username = username).exists():
           messages.error(request, "Username alreday exist!")  
           return redirect("register")
        else:
            if password == confirm_password:
                CustomUser.objects.create_user(username = username, password = password)
                return redirect('login')  
            else:
                error_message = "Passwords do not match."
                return render(request, 'register.html', {'error_message': error_message})

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
    return redirect('login')

def productadd(request):
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


def categoryadd(request):
        if request.method == 'POST':
          name = request.POST.get('name')
          Category.objects.create(name = name)
        return render(request,"categoryadd.html")

def product_view(request):
    products = Product.objects.all()
    return render(request,"product_view.html",{'products': products})

def product_detail(request, pk):
   
    product = get_object_or_404(Product, pk=pk)

   
    return render(request, 'product_detail.html', {'product': product})

def profile(request):
    return render("profile.html")

def update_profile(request):
        # last_name = request.POST.get('last_name')
        # first_name = request.POST.get('first_name')
        # email = request.POST.getlist('email')
        # dp = request.FILES.get('dp') 

    return render("update_profile.html")

def delete_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        product.delete()
        return redirect('product_view') 