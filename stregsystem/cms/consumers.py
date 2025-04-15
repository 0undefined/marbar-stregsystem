import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.contrib.auth.models import User
from .models import Marbar, MarbarConsumer, MarbarScore, get_active_marbar

class stregsystem_consumer(WebsocketConsumer):
    def connect(self):
        self.marbar = self.scope['url_route']['kwargs']['pk']
        self.room_group_name = 'marbar' + '-' + str(self.marbar)

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

        marbar = Marbar.objects.get(id=self.marbar)
        counters = Marbar.objects.get(marbar=marbar).annotate(score=Count('marbarscore__consumer')).values('marbarscore__consumer__name','score')
        self.send(text_data=json.dumps({
            'type': 'update_all',
            'streger': list({'consumer': kv['marbarscore__consumer__name'], 'count': kv['score']} for kv in counters)
        }))

    def disconnect(self, exit_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data, **kwargs):

        text_data_json = json.loads(text_data)
        kitchen = str(text_data_json.get('køkken', ""))

        if (kitchen != ""):
            genstande = int(text_data_json.get('streger', 0))

            self.send(text_data=json.dumps({'type': 'response', 'message': "ok", 'beers': genstande}))

            consumer = MarbarConsumer.objects.filter(name=kitchen)
            if (consumer.count() != 1):
                self.send(text_data=json.dumps({'type': 'response', 'message': "404: Consumer (kitchen) not found"}))
                return

            user = self.scope["user"]
            # TODO: Fix hardcoding id later, like the previous TODO
            MarbarScore(marbar=Marbar.objects.get(id=self.marbar), consumer=consumer[0], created_by=user).save()
            #counter = MarbarCounter.objects.get_or_create(marbar=Marbar.objects.get(id=self.marbar), consumer=consumer[0])
            #counter[0].counter += genstande
            #counter[0].save()

            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'update',
                    'consumer': kitchen,
                    'count': genstande,
                }
            )
        else:
            self.send(text_data=json.dumps({'type': 'response', 'message': "missing 'køkken' in message"}))

    def update(self, event):
        self.send(text_data=json.dumps(event))

    def update_all(self, event):
        self.send(text_data=json.dumps({'type': "update_all"}))
