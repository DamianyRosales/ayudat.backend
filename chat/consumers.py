import json
from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'for': text_data_json['for'],
                'from': text_data_json['from'],
                'content': text_data_json['content'],
                'time': text_data_json['time'],
                'channel': self.room_name
            }
        )

    # Receive message from room group

    async def chat_message(self, event):
        # message = event['message']
        print(event)
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'for': event['for'],
            'from': event['from'],
            'content': event['content'],
            'time': event['time'],
        }))
