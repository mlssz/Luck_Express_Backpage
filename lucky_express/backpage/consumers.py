"""
Consumers define function for websocket connecting, receiving messages
and disconnecting.
"""
from channels.generic.websockets import JsonWebsocketConsumer
from django.shortcuts import get_object_or_404

from backpage.models import User

class TestEchoConsumer(JsonWebsocketConsumer):
    "Service for echo messages."
    strict_ordering = False
    def receive(self, content, **kwargs):
        """
        ASGI WebSocket packet-received and send-packet message types
        both have a "text" key for their textual data.
        """
        self.send(content)

class TestLinkConsumer(JsonWebsocketConsumer):

    # Set to True if you want it, else leave it out
    strict_ordering = False

    def get_object(self, pk, token):
        """Get object and check the permissions of user."""
        try:
            obj = User.objects.get(pk=pk)
            if token != obj.token:
                return {
                    "state": 1,
                    "error": "Token Error: Hope {}, recieve {}.".format(obj.token, token)
                }
            else:
                return {"status": 0}

        except Exception as err:
            return {
                "state": 1,
                "error": "Uid Error: Not find user {}.".format(pk)
            }

    def connect(self, message, **kwargs):
        """
        Perform things on connection start
        """
        pk = kwargs.get("pk")
        token = kwargs.get("token")

        result = self.get_object(pk, token)
        self.send(result)

    def receive(self, content, **kwargs):
        """
        ASGI WebSocket packet-received and send-packet message types
        both have a "text" key for their textual data.
        """
        self.send({"message": "behavior not defined."})

class PositionsConsumer(JsonWebsocketConsumer):

    # Set to True if you want it, else leave it out
    strict_ordering = False

    def get_object(self, pk, token):
        """Get object and check the permissions of user."""
        try:
            obj = User.objects.get(pk=pk)
            if token != obj.token:
                return None
            else:
                return obj
        except Exception:
            return None

    def connect(self, message, **kwargs):
        """
        Perform things on connection start
        """
        pk = kwargs.get("pk")
        token = kwargs.get("token")

        obj = self.get_object(pk, token)

        if obj is None:
            message.reply_channel.send({"accept": False})
            self.close()

        print(message.reply_channel)

    def receive(self, content, **kwargs):
        """
        ASGI WebSocket packet-received and send-packet message types
        both have a "text" key for their textual data.
        """
        print(content['web'])
        self.send(content)

    def disconnect(self, message, **kwargs):
        """
        Perform things on connection close
        """
        print(message.reply_channel)
