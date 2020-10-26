from rest_framework import serializers


class UserSerializer(serializers.Serializer):
    """
    User Serializer
    """
    username = serializers.CharField(max_length=100, required=True)
    password = serializers.CharField(max_length=100, required=True)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class TimeLogSerializer(serializers.Serializer):
    """
    TimeLog Serializer
    """
    file_name = serializers.CharField(max_length=1000, required=True)
    file_extension = serializers.CharField(max_length=20, required=True)
    detected_language = serializers.CharField(max_length=50, required=True)
    log_date = serializers.DateField(required=True)
    log_timestamp = serializers.FloatField(required=True)
    api_token = serializers.CharField(max_length=200)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass
