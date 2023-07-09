from rest_framework import serializers
from .models import Shoes,Cart


class ShoeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shoes
        fields = "__all__"

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = "__all__"




