"""
Serializadores de Usuarios
Serializadores para los modelos de usuarios
"""
from rest_framework import serializers
from api.apps.users.models.users.user import User


class UserSerializer(serializers.ModelSerializer):
    """Serializador para usuarios"""
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'is_active', 'is_staff', 'is_superuser', 'date_joined',
            'last_login'
        ]
        read_only_fields = ['id', 'date_joined', 'last_login']


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializador para perfiles de usuario"""
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'phone', 'company', 'email_notifications', 'sms_notifications',
            'is_active', 'is_staff', 'is_superuser', 'date_joined', 'last_login'
        ]
        read_only_fields = ['id', 'date_joined', 'last_login']


class UserCreateSerializer(serializers.ModelSerializer):
    """Serializador para crear usuarios"""
    
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = [
            'username', 'email', 'first_name', 'last_name',
            'password', 'password_confirm'
        ]
    
    def validate(self, attrs):
        """Validar que las contraseñas coincidan"""
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Las contraseñas no coinciden")
        return attrs
    
    def create(self, validated_data):
        """Crear usuario con contraseña encriptada"""
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    """Serializador para actualizar usuarios"""
    
    class Meta:
        model = User
        fields = [
            'username', 'email', 'first_name', 'last_name',
            'is_active'
        ]


class UserPasswordChangeSerializer(serializers.Serializer):
    """Serializador para cambiar contraseña"""
    
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)
    new_password_confirm = serializers.CharField(write_only=True)
    
    def validate(self, attrs):
        """Validar contraseñas"""
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError("Las nuevas contraseñas no coinciden")
        return attrs


# Serializadores para endpoints específicos
class UserSummarySerializer(serializers.Serializer):
    """Serializador para resumen de usuarios"""
    
    total_users = serializers.IntegerField()
    active_users = serializers.IntegerField()
    staff_users = serializers.IntegerField()
    superusers = serializers.IntegerField()


class UserActivitySerializer(serializers.Serializer):
    """Serializador para actividad de usuarios"""
    
    user = UserSerializer()
    last_login = serializers.DateTimeField()
    login_count = serializers.IntegerField()
    owned_points = serializers.IntegerField() 