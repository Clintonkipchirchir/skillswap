from django.db import models
from rest_framework import viewsets, filters, status, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import User, UserSkill, Exchange, Feedback, Conversation, Message
from .serializers import (UserSerializer, UserSkillSerializer, 
                         ExchangeSerializer, FeedbackSerializer,
                         ConversationSerializer, MessageSerializer)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['username', 'skills__skill_name']
    filterset_fields = ['location']
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def skills(self, request, *args, **kwargs):
        user = self.get_object()
        skills = user.skills.all()
        serializer = UserSkillSerializer(skills, many=True)
        return Response(serializer.data)

class UserSkillViewSet(viewsets.ModelViewSet):
    serializer_class = UserSkillSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['skill_name']
    filterset_fields = ['is_offering', 'proficiency_level']
    
    def get_queryset(self):
        if self.action == 'list':
            return UserSkill.objects.all()
        return UserSkill.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def matches(self, request):
        """Find potential skill matches for the user"""
        # Get skills the user is seeking
        seeking_skills = request.user.skills.filter(is_offering=False).values_list('skill_name', flat=True)
        
        # Find users offering those skills
        potential_matches = UserSkill.objects.filter(
            skill_name__in=seeking_skills,
            is_offering=True
        ).exclude(user=request.user)
        
        # Check if those users are seeking skills the current user offers
        user_offering_skills = request.user.skills.filter(is_offering=True).values_list('skill_name', flat=True)
        
        matches = []
        for skill in potential_matches:
            # Check if this user is seeking any skills that the current user offers
            if UserSkill.objects.filter(
                user=skill.user,
                is_offering=False,
                skill_name__in=user_offering_skills
            ).exists():
                matches.append(skill)
        
        serializer = self.get_serializer(matches, many=True)
        return Response(serializer.data)

class ExchangeViewSet(viewsets.ModelViewSet):
    serializer_class = ExchangeSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status']
    
    def get_queryset(self):
        user = self.request.user
        return Exchange.objects.filter(
            models.Q(initiator=user) | models.Q(recipient=user)
        )
    
    def perform_create(self, serializer):
        serializer.save(initiator=self.request.user)
    
    @action(detail=True, methods=['post'])
    def accept(self, request, *args, **kwargs):
        exchange = self.get_object()
        if exchange.recipient != request.user:
            return Response({"detail": "Only the recipient can accept exchanges"}, 
                           status=status.HTTP_403_FORBIDDEN)
        
        exchange.status = 'accepted'
        exchange.save()
        return Response({"status": "exchange accepted"})
    
    @action(detail=True, methods=['post'])
    def complete(self, request, *args, **kwargs):
        exchange = self.get_object()
        if exchange.initiator != request.user and exchange.recipient != request.user:
            return Response({"detail": "Only participants can complete exchanges"}, 
                           status=status.HTTP_403_FORBIDDEN)
        
        exchange.status = 'completed'
        exchange.save()
        return Response({"status": "exchange completed"})

class FeedbackViewSet(viewsets.ModelViewSet):
    serializer_class = FeedbackSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Feedback.objects.filter(
            models.Q(reviewer=self.request.user) | models.Q(recipient=self.request.user)
        )
    
    def perform_create(self, serializer):
        exchange = serializer.validated_data['exchange']
        recipient = serializer.validated_data['recipient']
        
        
        if self.request.user != exchange.initiator and self.request.user != exchange.recipient:
            raise serializers.ValidationError("You can only leave feedback for exchanges you participated in")
        
        
        if recipient != exchange.initiator and recipient != exchange.recipient:
            raise serializers.ValidationError("The recipient must be a participant in the exchange")
        

        if self.request.user == recipient:
            raise serializers.ValidationError("You cannot leave feedback for yourself")
            
        serializer.save(reviewer=self.request.user)

class ConversationViewSet(viewsets.ModelViewSet):
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Conversation.objects.filter(participants=self.request.user)
    
    def perform_create(self, serializer):
        conversation = serializer.save()
        conversation.participants.add(self.request.user)
    
    @action(detail=True, methods=['get'])
    def messages(self, *args, **kwargs):
        conversation = self.get_object()
        messages = conversation.messages.all().order_by('created_at')
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Message.objects.filter(
            conversation__participants=self.request.user
        )
    
    def perform_create(self, serializer):
        conversation = serializer.validated_data['conversation']
        

        if not conversation.participants.filter(id=self.request.user.id).exists():
            raise serializers.ValidationError("You cannot send messages to this conversation")
            
        serializer.save(sender=self.request.user)