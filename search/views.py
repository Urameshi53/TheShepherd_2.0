from typing import Any, Dict
from django.db import models
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.contrib.auth.models import User
from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect
import datetime
from django.core.paginator import Paginator


from repository.models import File
from discussions.models import Discussion, Student
#from .mega import Search
from .finder import Search
from .forms import SearchForm
from home.models import Project



class IndexView(generic.ListView):
    template_name = "search/index.html"
    context_object_name = "search"
    #paginate_by = 3
    model = File
    #form = SearchForm()

    def get_queryset(self):
        return File.objects.all()
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super(IndexView, self).get_context_data(**kwargs)
        #context['discussions'] = Discussion.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]
        #context['discussions'] = Search.get_result()        
        context['files'] = File.objects.all()
        context['student'] = Student.objects.filter(user=self.request.user)[0]
        context['form'] = SearchForm(self.request.GET)
        context['discussions'] = Discussion.objects.all()
        context['projects'] = Project.objects.all()

        #print(context['form'].is_valid())
        if context['form'].is_valid():
            s = Search()
            query = context['form'].cleaned_data['query']
            context['sites'] = s.find_s(query)
            #print(context['results'])

        return context

