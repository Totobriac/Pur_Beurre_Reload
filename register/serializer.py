from rest_framework import serializers
from finder.models import SavedProduct, Product

class pagination(serializers.ModelSerializer):
    class Meta:
        fields = ('__all__')
        model = SavedProduct
        