from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView

from .models import Marbar
from .forms import MarbarForm

# Create your views here.
class index(ListView):
    template_name = 'cms/index.html'
    model = Marbar


class interface(TemplateView):
    template_name = 'cms/interface.html'


class new(CreateView):
    template_name = 'cms/new.html'
    #form_class = MarbarForm
    #success_url = '/index'
    model = Marbar
    fields = ['date_start', 'duration', 'title']

    def form_valid(self, form):
        return super().form_valid(form)
