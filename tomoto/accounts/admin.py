from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Customer, Order


admin.site.register(Customer, UserAdmin)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "customer_name",
        "phone",
        "total",
        "status",
        "created_at",
    )

    list_editable = ("status",)

    list_filter = ("status", "created_at")
    search_fields = ("customer_name", "phone")