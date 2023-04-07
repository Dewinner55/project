from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _


User = get_user_model() #для входа с лк юзера с активационным кодом


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password',) #исключено это поле


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=6, max_length=20, required=True, write_only=True)
    password2 = serializers.CharField(min_length=6, max_length=20, required=True, write_only=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'password2', 'last_name', 'first_name', 'username', 'avatar')

    def validate(self, attrs):
        password = attrs['password']
        password2 = attrs.pop('password2')
        if password != password2:
            raise serializers.ValidationError('Password didn\'t match!')
        if password.isdigit() or password.isalpha():
            raise serializers.ValidationError('Password field must contain alpha and numeric symbols!')
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class ActivationSerializer(serializers.Serializer):
    code = serializers.CharField(required=True, max_length=255)
    default_error_messages = {'bad_code': _('Link is expired or invalid!')} #токен просрочен

    def validate(self, attrs):
        self.code = attrs['code'] #сверка отправленного и вписанного кода активации
        return attrs

    def save(self, **kwargs):
        try:
            user = User.objects.get(activation_code=self.code)
            user.is_active = True
            user.activation_code = ''
            user.save()
        except User.DoesNotExist:
            self.fail('bad_code')













