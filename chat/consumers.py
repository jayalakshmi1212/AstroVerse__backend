import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from .models import Message,Notification
import asyncio
User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    active_peers = {}
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.peer_lock = asyncio.Lock() 
    async def connect(self):
        self.sender_id = self.scope['url_route']['kwargs']['sender_id']
        self.recipient_id = self.scope['url_route']['kwargs']['recipient_id']
        self.room_group_name = f"chat_{min(self.sender_id, self.recipient_id)}_{max(self.sender_id, self.recipient_id)}"


        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        print(f"WebSocket connected: {self.sender_id} -> {self.recipient_id}")

        # Fetch previous messages and send to the client
        previous_messages = await self.get_previous_messages()
        await self.send(text_data=json.dumps({
            'type': 'previous_messages',
            'messages': previous_messages
        }))

    async def disconnect(self, close_code):
        user_id = self.scope["url_route"]["kwargs"]["sender_id"]
        if user_id in self.active_peers:
            del self.active_peers[user_id]
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        
        print("WebSocket disconnected")

    async def receive(self, text_data):
        data = json.loads(text_data)
        print(data['type'],"dgjihdiufjndfjgn")
        if data['type'] == 'new_message':
            message = data['message']
            file_url = data.get('file_url', None)
            sender = await self.get_user(self.sender_id)
            recipient = await self.get_user(self.recipient_id)
            message_data = await self.create_message(sender, recipient, message,file_url)

            # Broadcast new message to the room
            await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message_data['message'],
                'sender': message_data['sender'],
                 'file_url': message_data['file_url'],
                'timestamp': message_data['timestamp']
            }
            
        )   
            notification_data = await self.create_notification(sender, recipient, message_data)
            await self.channel_layer.group_send(
                    f"user_{self.recipient_id}",  
                    {
                        'type': 'new_notification',
                        'sender': notification_data['sender'],
                        'message': notification_data['message'],
                        'timestamp': notification_data['timestamp'],
                        'is_read': notification_data['is_read']
                    }
                )
            
            
        elif data['type'] == 'typing':
            # Handle typing status
            is_typing = data['is_typing']
            username = await self.get_user(self.sender_id)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'typing_status',
                    'is_typing': is_typing,
                    'username': username.username
                }
            )
        elif data["type"] == "registerPeer":
            async with self.peer_lock:
                self.active_peers[data["userId"]] = data["peerId"]
            await self.send(text_data=json.dumps({"status": "Peer ID registered"}))

        elif data["type"] == "initiateCall":
            recipient_peer_id = self.active_peers.get(data["to"])
            if recipient_peer_id:
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        "type": "incomingCall",
                        "from": data["from"],
                        "peerId": data["peerId"]
                    }
                )
            else:
                await self.send(text_data=json.dumps({"error": "User is not available for a call"}))

        elif data["type"] == "answerCall":
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "callAccepted",
                    "to": data["to"]
                }
            )

        elif data["type"] == "endCall":
            await self.channel_layer.group_send(
                self.room_group_name,
                {"type": "endCall"}
            )
    
    async def chat_message(self, event):

        message = event['message']
        sender = event['sender']
        file_url=event.get('file_url',None)
        timestamp= event['timestamp']
        

        await self.send(text_data=json.dumps({
            'type': 'new_message',
            'message': message,
            'sender': sender,
            'file_url':file_url,
            'timestamp':timestamp
        }))

    async def typing_status(self, event):
        is_typing = event['is_typing']
        username = event['username']

        await self.send(text_data=json.dumps({
            'type': 'typing',
            'is_typing': is_typing,
            'username': username
        }))
        
   
    async def incomingCall(self, event):
        await self.send(text_data=json.dumps({"type": "incomingCall", "from": event["from"], "peerId": event["peerId"]}))

    async def callAccepted(self, event):
        await self.send(text_data=json.dumps({"type": "callAccepted", "to": event["to"]}))

    async def endCall(self, event):
        await self.send(text_data=json.dumps({"type": "endCall"}))
        
    async def new_notification(self, event):
        """Handles the notification event and sends it to the recipient."""
        await self.send(text_data=json.dumps({
            'type': 'new_notification',
            'sender': event['sender'],
            'message': event['message'],
            'timestamp': event['timestamp'],
            'is_read': event['is_read']
        }))

    @database_sync_to_async
    def get_user(self, user_id):
        return User.objects.get(id=user_id)

    @database_sync_to_async
    def create_message(self, sender, recipient, content,file_url):
        message = Message.objects.create(sender=sender, recipient=recipient, content=content,file_url=file_url)
        return {'message': message.content, 'sender': sender.username, 'file_url': file_url,'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S')}
    @database_sync_to_async
    def create_notification(self, sender, recipient, message_data):
        """Creates a notification for the recipient when a new message is received."""
        message_obj = Message.objects.get(content=message_data['message'])
        notification = Notification.objects.create(
            recipient=recipient,
            sender=sender,
            message=message_obj,
            is_read=False
        )
        return {
            'sender': sender.username,
            'message': message_data['message'],
            'timestamp': notification.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'is_read': notification.is_read
        }

    @database_sync_to_async
    def get_previous_messages(self):
        # Fetch messages where the sender or recipient matches the current users
        messages = Message.objects.filter(
            sender_id__in=[self.sender_id, self.recipient_id],
            recipient_id__in=[self.sender_id, self.recipient_id]
        ).order_by('timestamp')

        # Format messages as a list of dictionaries
        return [{'sender': msg.sender.username, 'message': msg.content,'file_url': msg.file_url,'timestamp': msg.timestamp.strftime('%Y-%m-%d %H:%M:%S')} for msg in messages]
