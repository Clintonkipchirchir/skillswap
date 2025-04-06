from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    
    def __str__(self):
        return self.username

class UserSkill(models.Model):
    SKILL_LEVELS = (
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('expert', 'Expert'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='skills')
    skill_name = models.CharField(max_length=100)
    description = models.TextField()
    proficiency_level = models.CharField(max_length=20, choices=SKILL_LEVELS)
    is_offering = models.BooleanField(default=True)  # True if offering, False if seeking
    
    class Meta:
        unique_together = ['user', 'skill_name', 'is_offering']
        
    def __str__(self):
        return f"{self.user.username} - {'Offering' if self.is_offering else 'Seeking'} {self.skill_name}"

class Exchange(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    
    initiator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='initiated_exchanges')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_exchanges')
    initiator_skill = models.ForeignKey(UserSkill, on_delete=models.CASCADE, related_name='offered_exchanges')
    recipient_skill = models.ForeignKey(UserSkill, on_delete=models.CASCADE, related_name='requested_exchanges')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.initiator.username} <-> {self.recipient.username}: {self.status}"

class Feedback(models.Model):
    RATING_CHOICES = [(i, i) for i in range(1, 6)]
    
    exchange = models.ForeignKey(Exchange, on_delete=models.CASCADE, related_name='feedbacks')
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='given_feedbacks')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_feedbacks')
    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['exchange', 'reviewer']
        
    def __str__(self):
        return f"{self.reviewer.username} -> {self.recipient.username}: {self.rating}/5"

class Conversation(models.Model):
    participants = models.ManyToManyField(User, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Conversation {self.id}"

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    content = models.TextField()
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.sender.username} in {self.conversation.id}: {self.content[:20]}..."