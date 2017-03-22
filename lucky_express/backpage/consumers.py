"""
Consumers define function for websocket connecting, receiving messages
and disconnecting.
"""
from channels.generic.websockets import JsonWebsocketConsumer
from django.shortcuts import get_object_or_404

from backpage.models import User
from backpage.datas import LesseeDM, RentalDM

def get_item_and_manager_of_pk(pk):
    item = RentalDM.getData(pk)
    if item is not None:
        return (item, RentalDM)

    item = LesseeDM.getData(pk)
    if item is not None:
        return (item, LesseeDM)

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

        if obj.user_type == 1:
            RentalDM.add(int(pk), 0, 0, message.reply_channel, [])
            message.reply_channel.send({"accept": True})
        elif obj.user_type == 2:
            LesseeDM.add(int(pk), 0, 0, message.reply_channel)
            message.reply_channel.send({"accept": True})
        else:
            message.reply_channel.send({"accept": False})
            self.close()

    def receive(self, content, **kwargs):
        """
        ASGI WebSocket packet-received and send-packet message types
        both have a "text" key for their textual data.
        """
        pk = int(kwargs.get("pk"))
        action = content.get("action", -1)

        item, manager = get_item_and_manager_of_pk(pk)

        if action == 99:
            positionx = content.get("positionx", None)
            positiony = content.get("positiony", None)
            px = item.position_x if positionx is None else positionx
            py = item.position_y if positiony is None else positiony
            manager.update(pk, position=(px, py))

    def disconnect(self, message, **kwargs):
        """
        Perform things on connection close
        """
        pk = int(kwargs.get("pk"))
        item, manager = get_item_and_manager_of_pk(pk)
        manager.deleteData(pk)
