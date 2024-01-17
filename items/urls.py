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
    path('user_detail/<int:pk>/',views.user_detail,name = "user_detail"), 
   path('product_detail/<int:pk>/',views.product_detail,name = "product_detail"), 
   path('product/delete/<int:product_id>/', views.delete_product, name='delete_product'),
   path('profile/',views.profile,name = "profile"),
   path('edit/<int:product_id>/',views.edit,name = "edit"),
   path('update_profile/',views.update_profile,name = "update_profile"),    
   path('edit_category/<int:category_id>/', views.edit_category, name='edit_category'),
   path('delete_category/<int:category_id>/', views.delete_category, name='delete_category'),
   path('email/',views.email,name = "email"),
]
 # path('productblog/<int:product_id>/', views.edit_product, name='editproduct'),
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)