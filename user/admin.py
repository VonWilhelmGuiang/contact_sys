from django.contrib import admin
from .models import Account

class AccountAdmin(admin.ModelAdmin):
    list_display = ('id','username','email','first_name','last_name')

admin.site.register(Account,AccountAdmin)
