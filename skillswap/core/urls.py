from django.urls import path
from .views import (
    CreateUserView,
    SkillListCreateView, SkillDetailView,
    ProfileListCreateView, ProfileDetailView,
    PostListCreateView, PostDetailView,
    MatchListCreateView, MatchDetailView,
    MessageListCreateView, MessageDetailView,
    ScheduleListCreateView, ScheduleDetailView,
    FeedbackListCreateView, FeedbackDetailView,
)



app_name = 'core'


urlpatterns = [
    path('api/users/register/', CreateUserView.as_view(), name='user-register'),
    path('api/skills/', SkillListCreateView.as_view(), name='skill-list-create'),
    path('api/skills/<int:pk>/', SkillDetailView.as_view(), name='skill-detail'),
    path('api/profiles/', ProfileListCreateView.as_view(), name='profile-list-create'),
    path('api/profiles/<int:pk>/', ProfileDetailView.as_view(), name='profile-detail'),
    path('api/posts/', PostListCreateView.as_view(), name='post-list-create'),
    path('api/posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('api/matches/', MatchListCreateView.as_view(), name='match-list-create'),
    path('api/matches/<int:pk>/', MatchDetailView.as_view(), name='match-detail'),
    path('api/messages/', MessageListCreateView.as_view(), name='message-list-create'),
    path('api/messages/<int:pk>/', MessageDetailView.as_view(), name='message-detail'),
    path('api/schedules/', ScheduleListCreateView.as_view(), name='schedule-list-create'),
    path('api/schedules/<int:pk>/', ScheduleDetailView.as_view(), name='schedule-detail'),
    path('api/feedbacks/', FeedbackListCreateView.as_view(), name='feedback-list-create'),
    path('api/feedbacks/<int:pk>/', FeedbackDetailView.as_view(), name='feedback-detail'),
]