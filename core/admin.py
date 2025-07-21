from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Permission, Role, UserRole, OTP

@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    # Fields to show in the list view
    list_display = ('email', 'phone', 'is_verified', 'is_staff')
    
    # Searchable fields
    search_fields = ('email', 'phone')
    
    # Filter options in the sidebar
    list_filter = ('is_staff', 'is_superuser', 'is_verified', 'is_active')
    
    ordering = ('email',)
    
    # Custom fieldsets to modify the edit form
    fieldsets = (
        (None, {'fields': ('password',)}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email', 'phone')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Custom Fields', {'fields': ('is_verified',)}),
    )
    
    # Optionally, restrict certain admin actions
    def has_delete_permission(self, request, obj=None):
        # Prevent deletion of superusers unless you're a superuser
        if obj and obj.is_superuser and not request.user.is_superuser:
            return False
        return super().has_delete_permission(request, obj)
    
admin.site.register(Permission)
admin.site.register(Role)
admin.site.register(UserRole)
@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):
    list_display = ('email', 'otp_code', 'created_at', 'is_verified')
    search_fields = ('email',)
    list_filter = ('is_verified',)
    ordering = ('-created_at',)