from rest_framework import serializers

class RegisterCustomerSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=255)
    last_name = serializers.CharField(max_length=255)
    phone_number = serializers.CharField(max_length=15)
    age = serializers.IntegerField()
    monthly_income = serializers.IntegerField()
