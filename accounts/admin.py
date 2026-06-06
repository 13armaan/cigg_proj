from django.contrib import admin
from .models import User , Role,EmailOTP

admin.site.register(User)
admin.site.register(Role)
admin.site.register(EmailOTP)
