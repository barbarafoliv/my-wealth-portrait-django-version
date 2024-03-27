from django.contrib import admin
from django.urls import path
from assets import views

urlpatterns = [
	path('logout/', views.custom_logout, name="logout"),
	path('report/', views.report , name='report'),
	path('admin/', admin.site.urls),
	path('login/' , views.login_page, name='login'),
	path('register/', views.register_page, name='register'),
	path('', views.assets, name='assets'),
	path('update_asset/<id>', views.update_asset, name='update_asset'),
	path('delete_asset/<id>', views.delete_asset, name='delete_asset'),
]

