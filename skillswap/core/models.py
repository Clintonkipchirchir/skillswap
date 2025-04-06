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


class Post(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=100)
    description = models.TextField()
    skills_offered = models.ManyToManyField(Skill, related_name='post_offered_skills', blank=True)
    skills_requested = models.ManyToManyField(Skill, related_name='post_requested_skills', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Match(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='matches')
    matched_with = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='matched_users')
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.post} -> {self.matched_with.user.username}"


class Message(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"From {self.sender.user.username} to {self.receiver.user.username}"


class Schedule(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='schedules')
    scheduled_time = models.DateTimeField()
    location = models.CharField(max_length=255)
    confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f"Session for {self.match}"


class Feedback(models.Model):
    giver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='given_feedbacks')
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='received_feedbacks')
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='feedbacks')
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])  # 1-5 star rating
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback by {self.giver.user.username} for {self.receiver.user.username}"

 