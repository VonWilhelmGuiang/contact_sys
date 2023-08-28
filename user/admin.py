from django.contrib import admin
from .models import Account, Contact


class AccountAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'first_name', 'last_name', 'active')
    list_display_links = ('id', 'username', 'email', 'first_name', 'last_name', 'active')
    search_fields = ('username', 'email', 'first_name', 'last_name')


class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_acc_name', 'first_name', 'last_name', 'phone', 'company', 'email')
    list_display_links = ('id', 'get_acc_name', 'first_name', 'last_name', 'phone', 'company', 'email')
    search_fields = ('get_acc_name','first_name', 'last_name', 'phone', 'company', 'email')

    @admin.display(description='Created By')
    def get_acc_name(self, obj):
        return obj.account_id.first_name +" "+obj.account_id.last_name

admin.site.register(Account, AccountAdmin)
admin.site.register(Contact, ContactAdmin)