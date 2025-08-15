from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    """User Profile model that extends Django's default User model."""

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")

    # User preferences stored as JSON
    preferences = models.JSONField(default=dict, blank=True)

    # Additional fields for better user management
    bio = models.TextField(max_length=500, blank=True)
    avatar = models.URLField(blank=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "api_user_profile"

    def get_preference(self, key, default=None):
        """Get a specific preference value."""
        return self.preferences.get(key, default)

    def set_preference(self, key, value):
        """Set a specific preference value."""
        if not self.preferences:
            self.preferences = {}
        self.preferences[key] = value
        self.save(update_fields=["preferences"])

    def update_preferences(self, preferences_dict):
        """Update multiple preferences at once."""
        if not self.preferences:
            self.preferences = {}
        self.preferences.update(preferences_dict)
        self.save(update_fields=["preferences"])

    def reset_preferences(self):
        """Reset preferences to default values."""
        self.preferences = {
            "theme": "auto",
            "colorScheme": "blue",
            "fontSize": "medium",
            "emailNotifications": True,
            "browserNotifications": True,
            "notifyScans": True,
            "notifyVulnerabilities": True,
            "notifyReports": True,
            "analytics": True,
            "sessionTimeout": "15",
            "twoFactor": False,
        }
        self.save(update_fields=["preferences"])

    def __str__(self):
        return f"Profile for {self.user.username}"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create a UserProfile when a new User is created."""
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Save the UserProfile when the User is saved."""
    if hasattr(instance, "profile"):
        instance.profile.save()
