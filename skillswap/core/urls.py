# core/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (UserViewSet, UserSkillViewSet, ExchangeViewSet, 
                   FeedbackViewSet, ConversationViewSet, MessageViewSet)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'skills', UserSkillViewSet, basename='skill')
router.register(r'exchanges', ExchangeViewSet, basename='exchange')
router.register(r'feedbacks', FeedbackViewSet, basename='feedback')
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'messages', MessageViewSet, basename='message')

urlpatterns = [
    path('', include(router.urls)),
]