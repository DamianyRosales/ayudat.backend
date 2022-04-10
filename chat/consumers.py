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
        print("1")

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'data' : text_data_json
            } 
        )

    # Receive message from room group

    async def chat_message(self, event): 
        # message = event['']
        # print(event)
        print("2")
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'for': event.data['for'],
            'from': event.data['from'],
            'content': event.data['content'],
            'time': event.data['time'],
        }))
        


        #  emitAMessage({
        #         for: currentContact.email,
        #         from: email,
        #         content: message,
        #         time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        #     }); 

