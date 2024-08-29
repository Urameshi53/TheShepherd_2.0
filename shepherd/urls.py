"""
URL configuration for shepherd project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from discussions.views import IndexView
from accounts.views import login, signup_view
from home.models import Project 
from discussions.models import Discussion, Student

from rest_framework import routers, serializers, viewsets


# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User 
        fields = ['url', 'username', 'email', 'is_staff']

# ViewSets define the view behavior
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer 


#class ProjectSerializer(serializers.HyperlinkedModelSerializer):
#    class Meta:
#       model = Project
#        fields = '__all__'

# ViewSets define the view behavior
#class ProjectViewSet(viewsets.ModelViewSet):
#    queryset = Project.objects.all()
#    serializer_class = ProjectSerializer 


#class DiscussionSerializer(serializers.HyperlinkedModelSerializer):
#    class Meta:
#        model = Discussion 
#        fields = '__all__'

# ViewSets define the view behavior
#class DiscussionViewSet(viewsets.ModelViewSet):
#    queryset = Discussion.objects.all()
#    serializer_class = DiscussionSerializer 


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
#router.register(r'projects', ProjectViewSet)
#router.register(r'discussions', DiscussionViewSet)


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', login, name='login'),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('accouts/signup/', signup_view, name='signup'),
    path("discussions/", IndexView.as_view(), name="home"),
    path('discussions/', include('discussions.urls')),
    path('repository/', include('repository.urls')),
    path('search/', include('search.urls')),
    path('home/', include('home.urls')),
    path('sliders/', include('sliders.urls')),
    path('projects/', include('projects.urls')),
    path('admin/', admin.site.index , name='admin'),
    path('admin/', admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
    path('api-auth/', include('rest_framework.urls'))
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
