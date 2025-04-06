from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, UserSkill, Exchange, Feedback, Conversation, Message

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'location', 'is_staff')
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Profile Information', {'fields': ('bio', 'location', 'profile_picture')}),
    )

@admin.register(UserSkill)
class UserSkillAdmin(admin.ModelAdmin):
    list_display = ('user', 'skill_name', 'proficiency_level', 'is_offering')
    list_filter = ('is_offering', 'proficiency_level')
    search_fields = ('user__username', 'skill_name')

@admin.register(Exchange)
class ExchangeAdmin(admin.ModelAdmin):
    list_display = ('initiator', 'recipient', 'status', 'created_at', 'updated_at')
    list_filter = ('status',)
    search_fields = ('initiator__username', 'recipient__username')
    date_hierarchy = 'created_at'

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('reviewer', 'recipient', 'rating', 'created_at')
    list_filter = ('rating',)
    search_fields = ('reviewer__username', 'recipient__username', 'comment')

@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'updated_at')
    filter_horizontal = ('participants',)
    
    def get_participants(self, obj):
        return ", ".join([user.username for user in obj.participants.all()])
    get_participants.short_description = 'Participants'

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'conversation', 'content_preview', 'read', 'created_at')
    list_filter = ('read', 'created_at')
    search_fields = ('sender__username', 'content')
    
    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content'