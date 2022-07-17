from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView

from .models import Marbar
from .forms import MarbarForm

# Create your views here.
class index(ListView):
    template_name = 'cms/index.html'
    model = Marbar

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['active'] = list(filter(
            lambda m: m.date_end > timezone.now(),
            Marbar.objects.filter(date_start__lt=timezone.now()).order_by('-date_start')))

        return context


class interface(TemplateView):
    template_name = 'cms/interface.html'


class view(DetailView):
    model = Marbar

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        context['ends'] = self.object.date_end
        return context
    #form_class = MarbarForm
    #success_url = '/index'
    #fields = ['date_start', 'duration', 'title']

    #def form_valid(self, form):
    #    return super().form_valid(form)


class new(CreateView):
    #form_class = MarbarForm
    #success_url = '/index'
    model = Marbar
    fields = ['date_start', 'duration', 'title']

    def form_valid(self, form):
        return super().form_valid(form)


class edit(UpdateView):
    model = Marbar
    # We use the list instead of '__all__' to define the order :)
    fields = ['title', 'banner', 'date_start', 'duration', 'extra_hours', 'note', 'style']


def add_drinks(request):
    return JsonResponse({})


class interface(TemplateView):
    template_name = 'cms/interface.html'


def view_active(request):
    active = None
    context = {}

    # Get latest marbar with date_start prior to now
    marbars = Marbar.objects.filter(date_start__lt=timezone.now()).order_by('-date_start').first()

    # Get next marbar with date_start later than now
    upcoming_marbar = Marbar.objects.filter(date_start__gt=timezone.now()).order_by('-date_start').first()

    if (marbars.date_end > timezone.now()):
        active = marbars
    elif (upcoming_marbar is not None):
        active = upcoming_marbar

    context['object'] = active
    return render(request, 'cms/marbar_detail.html', context)
