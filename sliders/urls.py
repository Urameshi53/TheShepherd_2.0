from django.urls import path 
from django.conf import settings
from django.conf.urls.static import static

from . import views 

app_name = "sliders"

urlpatterns = [
    path("", views.IndexView.as_view(), name="sliders"),
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("<int:user_id>/request_book/", views.request_book , name="request_book"),
    path("<int:request_id>/contribute_book/", views.contribute_book , name="contribute_book"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
