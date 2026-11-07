from django.contrib import admin
from .models import Users

@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = ("id", "account_number", "name", "phone_number", "amount")
    search_fields = ("account_number", "name", "phone_number")
    list_filter = ("gender",)
    # Never expose password hashes in the admin list.
