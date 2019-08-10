from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404

from apps.engineering.serializers import ProjectSerializer
from apps.warehouse.models import Warehouse, Stock, StockRelease


class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = "__all__"


class StockSerializer(serializers.ModelSerializer):
    warehouse = WarehouseSerializer()

    class Meta:
        model = Stock
        fields = "__all__"


class CreateStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = "__all__"


class StockReleaseSerializer(serializers.ModelSerializer):
    warehouse = WarehouseSerializer()
    stock = StockSerializer()
    project = ProjectSerializer()

    class Meta:
        model = StockRelease
        fields = "__all__"


class CreateStockReleaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockRelease
        fields = "__all__"

    def validate(self, data):
        print(data.get('stock'))
        if data.get('quantity') > data.get('stock').stock:
            raise ValidationError('Quantity is greater than stock available.')

        return data

    def create(self, validated_data):
        stock_id = validated_data['stock']
        quantity = validated_data['quantity']
        print(validated_data)
        stocks = stock_id

        stock_release = super().create(validated_data)
        stocks.stock = stocks.stock - quantity
        stocks.save()

        return stock_release
