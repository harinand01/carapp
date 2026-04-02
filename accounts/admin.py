from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Customer, Mechanic

class MechanicInline(admin.StackedInline):
    model = Mechanic
    can_delete = False
    verbose_name_plural = 'Mechanic Profile'

class CustomUserAdmin(UserAdmin):
    inlines = (MechanicInline,)

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Customer)
admin.site.register(Mechanic)

