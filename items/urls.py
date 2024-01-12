from django.urls import path
from . import views

urlpatterns = [
   path('',views.home,name='home'),
   path('login',views.user_login,name = "login"),
   path('logout',views.user_logout,name = "logout"),
   path('register/',views.register,name = "register"),    
   path('categoryadd/',views.categoryadd,name = "categoryadd"),  
   path('productadd/',views.productadd,name = "productadd"),  
   path('product_view/',views.product_view,name = "product_view"), 
   path('product_detail/<int:pk>/',views.product_detail,name = "product_detail"), 
    path('product/delete/<int:product_id>/', views.delete_product, name='delete_product'),
  
]
 # path('productblog/<int:product_id>/', views.edit_product, name='editproduct'),
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)