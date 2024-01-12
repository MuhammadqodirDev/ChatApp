import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']



        # Broadcast the received message to all connected clients
        await self.channel_layer.group_add("chat", self.channel_name)
        await self.channel_layer.group_send(
            "chat",
            {
                "type": "chat.message",
                "message": message,
            },
        )
        

    async def chat_message(self, event):
        message = event['message']

        # Send the message to the WebSocket
        await self.send(text_data=json.dumps({'message': message}))

