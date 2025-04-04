from django.contrib import admin
from django.contrib.auth.models import Group, User
from .models import Profile, Skill

# unregister groups
admin.site.unregister(Group)


# Register your models here.
class ProfileInline(admin.StackedInline):
    model = Profile
    verbose_name_plural = 'Profile'
    # This widget makes it easier to manage many-to-many relationships
    filter_horizontal = ('offered_skills', 'desired_skills',)



class UserAdmin(admin.ModelAdmin):
    model = User
    fields = ["username"]
    inlines = [ProfileInline]



# unregister initial user
admin.site.unregister(User)

# register new user
admin.site.register(User, UserAdmin)
admin.site.register(Profile)
admin.site.register(Skill)
