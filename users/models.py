from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    ACADEMIC_LEVEL_CHOICES = [
        ('Beginner', 'Beginner'),
        ('Undergraduate', 'Undergraduate'),
        ('MCA Student', 'MCA Student'),
        ('Researcher', 'Researcher'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    research_interests = models.TextField(blank=True, default='')
    academic_level = models.CharField(max_length=50, choices=ACADEMIC_LEVEL_CHOICES, default='MCA Student')
    avatar = models.CharField(max_length=50, default='technomancer')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile ({self.academic_level}, {self.avatar})"

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    else:
        if hasattr(instance, 'profile'):
            instance.profile.save()
