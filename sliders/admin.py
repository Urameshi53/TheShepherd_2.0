from django.contrib import admin
from .models import Request, Contribution

# Register your models here.
admin.site.register(Request)
admin.site.register(Contribution)