from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Skill(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=30, blank=True)
    offered_skills = models.ManyToManyField(Skill, blank=True, related_name='offered')
    desired_skills = models.ManyToManyField(Skill, blank=True, related_name='desired')
    

    def __str__(self):
        return self.user.username
    

 