from django.contrib import admin
from .models import User, Permission, Role, UserRole, OTP

admin.site.register(User)
admin.site.register(Permission)
admin.site.register(Role)
admin.site.register(UserRole)
admin.site.register(OTP)