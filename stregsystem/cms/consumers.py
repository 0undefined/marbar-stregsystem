import json
from channels.generic.websocket import WebsocketConsumer

class stregsystem_consumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, exit_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        kitchen = str(text_data_json['køkken'])
        genstande = int(text_data_json['streger'])

        self.send(text_data=json.dumps({'message': "ok", 'beers': genstande}))
