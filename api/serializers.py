from rest_framework import serializers
from api_dev.models import Email

class Memberserializer(serializers.ModelSerializer):
    class Meta:
        model = Email
        fields = '__all__'