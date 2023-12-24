from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .models import ActivityLog

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'SecurityQuestion']

    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('SecurityQuestion', 'SecurityQuestionAnswer', 'passwords_history')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)

class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'activity', 'timestamp']
    list_filter = ['timestamp']

    def has_change_permission(self, request, obj=None):
        # Only superusers have permission to change activity logs
        if request.user.is_superuser:
            return True
        return False


admin.site.register(ActivityLog, ActivityLogAdmin)