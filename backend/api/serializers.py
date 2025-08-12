from core.models.user_profile import UserProfile
from django.contrib.auth.models import User
from django.utils import timezone
from djoser.serializers import UserSerializer
from rest_framework import serializers


class CustomUserSerializer(UserSerializer):
    preferences = serializers.SerializerMethodField()
    date_joined = serializers.SerializerMethodField()
    last_login = serializers.SerializerMethodField()

    class Meta(UserSerializer.Meta):
        model = User
        fields = ("id", "username", "email", "date_joined", "last_login", "preferences")
        read_only_fields = ("id", "date_joined", "last_login")

    def get_preferences(self, obj):
        """Get user preferences from UserProfile."""
        if hasattr(obj, "profile"):
            return obj.profile.preferences
        return {}

    def get_date_joined(self, obj):
        """Format date_joined properly."""
        if obj.date_joined:
            # Format as ISO string
            return obj.date_joined.isoformat()
        return None

    def get_last_login(self, obj):
        """Format last_login properly."""
        if obj.last_login:
            # Format as ISO string
            return obj.last_login.isoformat()
        return None


class UserPreferencesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ("preferences",)

    def update(self, instance, validated_data):
        preferences = validated_data.get("preferences", {})
        instance.update_preferences(preferences)
        return instance


class ChangeEmailSerializer(serializers.Serializer):
    current_email = serializers.EmailField()
    new_email = serializers.EmailField()
    current_password = serializers.CharField(write_only=True)

    def validate_current_email(self, value):
        user = self.context["request"].user
        if user.email != value:
            raise serializers.ValidationError(
                "Current email does not match your account email."
            )
        return value

    def validate_new_email(self, value):
        user = self.context["request"].user
        if User.objects.filter(email=value).exclude(id=user.id).exists():
            raise serializers.ValidationError("This email is already in use.")
        return value

    def validate(self, attrs):
        user = self.context["request"].user
        if not user.check_password(attrs["current_password"]):
            raise serializers.ValidationError("Current password is incorrect.")
        return attrs
