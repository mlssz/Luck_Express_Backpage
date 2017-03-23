"""lucky_express serializers define.

lucky express implement all api about map positions.

api docs please see:
    https://mlssz.github.io/apiDoc/apiForPassenger

"""
from rest_framework import serializers

from backpage.models import (
    Orders,
    User,
    Rental,
    Lessee
)

class UserSerializer(serializers.ModelSerializer):
    """User serializer."""
    class Meta:
        model = User
        fields = ("id", "account", "name", "signup_time", "pre_login_time", "token", "user_type")


class LesseeSerializer(serializers.ModelSerializer):
    """For receiving postion of render."""
    id = UserSerializer(read_only=True)
    truck = serializers.SlugRelatedField(
            read_only=True,
            slug_field="no"
        )

    class Meta:
        model = Lessee
        fields = ("position_x", "position_y", "score", "order_count", "id", "truck")

class RentalSerializer(serializers.ModelSerializer):
    """For receiving postion of render."""
    id = serializers.SlugRelatedField(
        slug_field="account",
        read_only=True
    )

    class Meta:
        model = Rental
        fields = ("position_x", "position_y", "score", "id")

class OrderSerializer(serializers.ModelSerializer):
    rental = RentalSerializer(read_only=True)

    class Meta:
        model = Orders
        fields = ("id", "rental", "lessee", "starttime", "endtime", "startplace", "startplacex",
                  "startplacey", "endplace", "fee", "score", "accepttime", "finishtime", "remark",
                  "remark", "trucktype", "status")
