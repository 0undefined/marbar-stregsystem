from django.http import JsonResponse
from django.utils import timezone
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from django.contrib.auth.views import LoginView

import logging

logger = logging.getLogger(__name__)

from .models import Marbar, MarbarScore, MarbarConsumer, get_active_marbar
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active'] = get_active_marbar()
        return context


class view(DetailView):
    model = Marbar

    get_active = False

    def get_object(self, queryset=None):
        if self.get_active:
            return get_active_marbar()
        else:
            return super(view, self).get_object(queryset=queryset)

    def get_context_data(self, **kwargs):
        context         = super().get_context_data(**kwargs)
        context['now']  = timezone.now()
        if (self.object is not None):
            context['ends'] = self.object.date_end
        return context


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
    fields = ['title', 'banner', 'date_start', 'duration', 'extra_hours',
              'note', 'style', 'elfsight_apikey']


class login(LoginView):
    pass


def marbar(request, marbar_id):
    if request.method == 'GET':
        from django.db.models import Count
        from django.db.models import F

        return JsonResponse(
            dict((k['consumer'],k['score']) for k in list( Marbar.objects.filter(id=marbar_id).annotate(score=Count('marbarscore__consumer'), consumer=F('marbarscore__consumer__name')).values('consumer','score')))
        )
    elif request.method == 'POST':
        from django.contrib.auth.models import User
        from django.http import HttpResponseForbidden
        import json
        body = json.loads(request.body)

        consumer = body.get("køkken", "")
        count = int(body.get("streger", 0))
        user = request.user

        if not consumer:
            return JsonResponse({'status': "error", 'message': "invalid consumer", 'data': str(request.body)})

        #if not user.is_authenticated:
        #    return HttpResponseForbidden()

        c = MarbarConsumer.objects.get(name=consumer)
        u = User.objects.get(username=user.username)

        for s in range(count):
            MarbarScore(marbar=Marbar.objects.get(id=marbar_id), consumer=c, created_by=user).save()

        return JsonResponse({})


def add_drinks(request):
    return JsonResponse({})


class interface(TemplateView):
    template_name = 'cms/interface.html'

    def get_context_data(self, **kwargs):
        context           = super().get_context_data(**kwargs)
        context['marbar'] = get_active_marbar()
        return context


class consumer_index(ListView):
    model = MarbarConsumer


class consumer_new(CreateView):
    model = MarbarConsumer
    fields = ['name']
