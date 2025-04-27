from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from accounts.models import User, Company, Contact
from django.utils.translation import gettext_lazy as _

admin.site.unregister(Group)


@admin.register(User)
class UserAdmin(UserAdmin):
    fieldsets = (
        (None, {"fields": ("id", "api_id", "username", "password")}),
        (
            _("Personal info"),
            {"fields": ("first_name", "last_name", "email", "company", "contact")},
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "usable_password", "password1", "password2"),
            },
        ),
    )
    autocomplete_fields = ("company", "contact")


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("id", "api_id", "name", "contact")
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "api_id",
        "phone_number",
        "postal_code",
        "city",
        "state",
        "country",
    )
    search_fields = ("phone_number", "postal_code", "city", "state", "country")
    ordering = ("city",)
