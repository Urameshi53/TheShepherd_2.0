from django.urls import path
from .views import ProfileView

from . import views

app_name = 'accounts'

urlpatterns = [
    path('index/', views.login, name='index'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path("signup/", views.signup_view, name='signup'),
    path('reset/', views.reset_view, name='reset'),
    path('<int:user_id>/discuss/', views.discuss_view, name='discuss'),
    path('<int:pk>/', ProfileView.as_view(), name='profile'),
    path('<int:user_id>/reset/', views.reset_view, name='reset')
]