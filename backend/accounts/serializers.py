from rest_framework import serializers
from django.contrib.auth import get_user_model
from hospitals.models import Hospital

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'email', 'name', 'role', 'hospital', 'is_active']
        read_only_fields = ['user_id']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    hosName = serializers.CharField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'role', 'hosName']

    def create(self, validated_data):
        hospital_name = validated_data.pop('hosName', None)
        hospital = None
        
        if hospital_name:
            hospital, created = Hospital.objects.get_or_create(
                name=hospital_name,
                defaults={'location': 'Unknown'} # Needed since location is required on Hospital model
            )
            
        validated_data['hospital'] = hospital
        # Default name to email prefix since frontend doesn't provide it yet
        validated_data['name'] = validated_data['email'].split('@')[0]

        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            role=validated_data['role'],
            name=validated_data['name'],
            hospital=validated_data.get('hospital')
        )
        return user

class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'email', 'name', 'role', 'hospital', 'is_active', 'is_staff']
        read_only_fields = ['user_id', 'email', 'role', 'is_staff']
