from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView

from .models import Marbar
from .forms import MarbarForm

# Create your views here.
class index(ListView):
    template_name = 'cms/index.html'
    model = Marbar


class interface(TemplateView):
    template_name = 'cms/interface.html'


class view(DetailView):
    template_name = 'cms/view.html'
    model = Marbar

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        context['ends'] = self.object.date_start + self.object.duration
        return context
    #form_class = MarbarForm
    #success_url = '/index'
    #fields = ['date_start', 'duration', 'title']

    #def form_valid(self, form):
    #    return super().form_valid(form)


class new(CreateView):
    template_name = 'cms/new.html'
    #form_class = MarbarForm
    #success_url = '/index'
    model = Marbar
    fields = ['date_start', 'duration', 'title']

    def form_valid(self, form):
        return super().form_valid(form)
