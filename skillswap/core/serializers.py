from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Profile, Skill, Post, Match, Message, Schedule, Feedback


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password']
        extra_kwargs = {"password": {"write_only": True}}

    def create(self ,validate_data):
        user = User.objects.create_user(**validate_data)
        return user

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['id', 'name', 'description']


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    offered_skills = SkillSerializer(many=True, read_only=True)
    desired_skills = SkillSerializer(many=True, read_only=True)

    class Meta:
        model = Profile
        fields = ['id', 'user', 'bio', 'location', 'offered_skills', 'desired_skills']


class PostSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)
    skills_offered = SkillSerializer(many=True, read_only=True)
    skills_requested = SkillSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'profile', 'title', 'description', 'skills_offered', 'skills_requested', 'created_at']


class MatchSerializer(serializers.ModelSerializer):
    post = PostSerializer(read_only=True)
    matched_with = ProfileSerializer(read_only=True)

    class Meta:
        model = Match
        fields = ['id', 'post', 'matched_with', 'status', 'created_at']


class MessageSerializer(serializers.ModelSerializer):
    sender = ProfileSerializer(read_only=True)
    receiver = ProfileSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'sender', 'receiver', 'content', 'timestamp', 'is_read']


class ScheduleSerializer(serializers.ModelSerializer):
    match = MatchSerializer(read_only=True)

    class Meta:
        model = Schedule
        fields = ['id', 'match', 'scheduled_time', 'location', 'confirmed']


class FeedbackSerializer(serializers.ModelSerializer):
    giver = ProfileSerializer(read_only=True)
    receiver = ProfileSerializer(read_only=True)
    match = MatchSerializer(read_only=True)

    class Meta:
        model = Feedback
        fields = ['id', 'giver', 'receiver', 'match', 'rating', 'comment', 'created_at']
