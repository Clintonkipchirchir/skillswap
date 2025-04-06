from rest_framework import serializers
from .models import User, UserSkill, Exchange, Feedback, Conversation, Message

class UserSkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSkill
        fields = ['id', 'skill_name', 'description', 'proficiency_level', 'is_offering']

class UserSerializer(serializers.ModelSerializer):
    skills = UserSkillSerializer(many=True, read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'bio', 'location', 'profile_picture', 'skills']
        extra_kwargs = {'password': {'write_only': True}}
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class FeedbackSerializer(serializers.ModelSerializer):
    reviewer_username = serializers.ReadOnlyField(source='reviewer.username')
    recipient_username = serializers.ReadOnlyField(source='recipient.username')
    
    class Meta:
        model = Feedback
        fields = ['id', 'exchange', 'reviewer', 'reviewer_username', 'recipient', 
                 'recipient_username', 'rating', 'comment', 'created_at']

class ExchangeSerializer(serializers.ModelSerializer):
    initiator_username = serializers.ReadOnlyField(source='initiator.username')
    recipient_username = serializers.ReadOnlyField(source='recipient.username')
    feedbacks = FeedbackSerializer(many=True, read_only=True)
    
    class Meta:
        model = Exchange
        fields = ['id', 'initiator', 'initiator_username', 'recipient', 'recipient_username',
                 'initiator_skill', 'recipient_skill', 'status', 'created_at', 'updated_at', 'feedbacks']

class MessageSerializer(serializers.ModelSerializer):
    sender_username = serializers.ReadOnlyField(source='sender.username')
    
    class Meta:
        model = Message
        fields = ['id', 'conversation', 'sender', 'sender_username', 'content', 'read', 'created_at']

class ConversationSerializer(serializers.ModelSerializer):
    participants_detail = UserSerializer(source='participants', many=True, read_only=True)
    latest_messages = serializers.SerializerMethodField()
    
    class Meta:
        model = Conversation
        fields = ['id', 'participants', 'participants_detail', 'created_at', 'updated_at', 'latest_messages']
    
    def get_latest_messages(self, obj):
        
        messages = obj.messages.order_by('-created_at')[:5]
        return MessageSerializer(messages, many=True).data