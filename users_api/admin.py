from django.contrib import admin

from users_api.models import UserBase, Admin, Mod, Professional, Patient
# Register your models here.

admin.site.register(UserBase)
admin.site.register(Admin)
admin.site.register(Mod)
admin.site.register(Professional)
admin.site.register(Patient)
