import json

from django.http import JsonResponse, HttpResponseForbidden, HttpResponseNotFound
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import User, Group

import logging

logger = logging.getLogger(__name__)

from .models import Marbar, MarbarScore, MarbarConsumer, get_active_marbar, MarbarParticipant
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

    def get_context_data(self, **kwargs):
        context         = super().get_context_data(**kwargs)
        kitchens = Group.objects.get(name='kitchen').user_set.all()
        kitchens = [{
            'id': user.id,
            'username': user.username,
            'role': MarbarParticipant.default_participation(self.object, user),
        } for user in kitchens]
        context['kitchens'] = kitchens
        context['roles'] = MarbarParticipant.Role
        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        self.object = self.get_object()

        # Update participants
        roles = [(k,v[0]) for k,v in dict(request.POST).items() if k.startswith('kitchen-')]


        # We make sure that we do not create new participants if they was
        # disabled before, like a soft deletion.
        for role in filter(lambda r: r[1] != "Disabled", roles):
            u = User.objects.get(username=role[0][len('kitchen-'):])
            p = MarbarParticipant.objects.get_or_create(marbar=self.object, user=u)[0]
            p.role = list(filter(lambda r: r[1] == role[1], MarbarParticipant.Role.choices))[0][0]
            p.save()
        for role in filter(lambda r: r[1] == "Disabled", roles):
            u = User.objects.get(username=role[0][len('kitchen-'):])
            p = MarbarParticipant.objects.filter(marbar=self.object, user=u)
            if len(p) == 1:
                p = p.first()
                p.role = MarbarParticipant.Role.DISABLED.value
                p.save()
        return super().post(request, *args, **kwargs)


class userlist(ListView):
    model = User
    def get_context_data(self,*args, **kwargs):
        context = super(userlist, self).get_context_data(*args,**kwargs)
        context['kitchengroup'] = set(a[0] for a in Group.objects.get_or_create(name='kitchen')[0].user_set.all().values_list('username'))
        context['object_list'] = context['object_list'].order_by('-is_active', 'groups__name', 'date_joined')
        context['users_active'] = User.objects.filter(is_active=True)
        context['users_inactive'] = User.objects.filter(is_active=False)

        return context

    def post(self, request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            return HttpResponseForbidden()


        #u = User.objects.get(request.POST
        user_deactivate_id = [k for k,v in dict(request.POST).items() if v == ['Deactivate']]
        user_activate_id = [k for k,v in dict(request.POST).items() if v == ['Activate']]
        new_kitchen = request.POST.get('kitchen_name', "")

        if len(user_deactivate_id) == 1 and len(user_activate_id) == 1:
            return HttpResponseNotFound('Invalid input' + str(request.POST))
        elif len(user_deactivate_id) == 1:
            u = get_object_or_404(User, id=user_deactivate_id[0])
            u.is_active = False
            u.save()
        elif len(user_activate_id) == 1:
            u = get_object_or_404(User, id=user_activate_id[0])
            u.is_active = True
            u.save()
        elif len(new_kitchen) > 1:
            group_kitchens = Group.objects.get_or_create(name='kitchen')[0]
            group_kitchens.user_set.add(
                User.objects.get_or_create(username=new_kitchen)[0]
            )
        else:
            return JsonResponse({'post':str(dict(request.POST).items()), 'k': new_kitchen})
            return HttpResponseNotFound('Invalid input' + str(request.POST))

        #return JsonResponse({'post':str(request.POST), 'uid':u.username})
        return super(userlist, self).get(request, *args, **kwargs)


def marbar(request, marbar_id):
    if request.method == 'GET':
        from django.db.models import Count
        from django.db.models import F

        return JsonResponse(
            dict((k['consumer'],k['score']) for k in list( Marbar.objects.filter(id=marbar_id).annotate(score=Count('marbarscore__consumer'), consumer=F('marbarscore__consumer__name')).values('consumer','score')))
        )
    elif request.method == 'POST':
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

        return JsonResponse({'status': "ok"})


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
