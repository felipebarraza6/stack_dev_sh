# Django REST Framework
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator

# Django
from django.contrib.auth import password_validation, authenticate
from django.core.validators import RegexValidator

# Models
from api.core_app.models import User, ProfileClient, RegisterPersons


class RegisterPersonSerializers(serializers.ModelSerializer):
    class Meta:
        model = RegisterPersons
        fields = '__all__'


class UserInfoModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('__all__')


class Profile(serializers.ModelSerializer):
    persons = serializers.SerializerMethodField('get_persons')

    def get_persons(self, profile):
        qs = RegisterPersons.objects.filter(profile=profile.id)
        serializer = RegisterPersonSerializers(instance=qs, many=True)
        data = serializer.data
        return data

    class Meta:
        model = ProfileClient
        fields = '__all__'


class UserProfile(serializers.ModelSerializer):
    profile_data = serializers.SerializerMethodField('get_profile')

    def get_profile(self, user):
        qs = ProfileClient.objects.filter(user=user.id)
        serializer = Profile(instance=qs, many=True)
        data = serializer.data
        return data

    class Meta:
        model = User
        fields = '__all__'


class UserModelSerializer(serializers.ModelSerializer):
    profile_data = serializers.SerializerMethodField('get_profile')

    def get_profile(self, user):
        qs = ProfileClient.objects.filter(user=user.id)
        serializer = Profile(instance=qs, many=True)
        data = serializer.data
        return data

    class Meta:
        model = User
        fields = '__all__'


class UserLoginSerializer(serializers.Serializer):

    email = serializers.EmailField()
    password = serializers.CharField(min_length=8, max_length=64)

    def validate(self, data):
        user = authenticate(username=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError('Credenciales Invalidas')
        if not user.is_verified:
            raise serializers.ValidationError(
                'Cuenta de usuario aun no verificada')
        self.context['user'] = user
        return data

    def create(self, data):
        token, created = Token.objects.get_or_create(user=self.context['user'])
        return self.context['user'], token.key


class UserSignUpSerializer(serializers.Serializer):

    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    username = serializers.CharField(
        min_length=4,
        max_length=20,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(min_length=8, max_length=64)
    password_confirmation = serializers.CharField(min_length=8, max_length=64)

    def validate(self, data):
        passwd = data['password']
        passwd_conf = data['password_confirmation']
        if passwd != passwd_conf:
            raise serializers.ValidationError("Contraseñas no coinciden")
        password_validation.validate_password(passwd)
        return data

    def create(self, data):
        data.pop('password_confirmation')
        user = User.objects.create_user(**data, is_active=True)
        return user
