
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.signup),
    path('login/', views.user_login),
    path('signup/', views.signup),
    path('todopage/', views.todopage, name='todopage'),
    path('logout/', views.logout),
    path('delete_todo/<int:srno>/', views.delete_todo, name='delete_todo'),
    path('edit_todo/<int:srno>/', views.edit_todo, name='edit_todo'),
]
