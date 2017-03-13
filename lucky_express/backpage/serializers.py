"""lucky_express serializers define.

lucky express implement all api about map positions.

api docs please see:
    https://mlssz.github.io/apiDoc/apiForPassenger

"""
from rest_framework import serializers

from backpage.models import User, Lessee

class UserSerializer(serializers.ModelSerializer):
    """User serializer."""
    class Meta:
        model = User
        fields = ("id", "account", "name", "signup_time", "pre_login_time", "token", "user_type")

class LesseeSerializer(serializers.ModelSerializer):
    """For receiving postion of render."""
    id = UserSerializer(read_only=True)

    class Meta:
        model = Lessee
        fields = ("position_x", "position_y", "score", "order_count","id")
