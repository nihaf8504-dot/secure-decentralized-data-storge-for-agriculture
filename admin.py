from django.contrib import admin
from .models import Block, AuditLog


# -----------------------------
# BLOCK ADMIN (DEMO TAMPERING ENABLED)
# -----------------------------
@admin.register(Block)
class BlockAdmin(admin.ModelAdmin):
    list_display = (
        'index',
        'user',
        'timestamp',
        'hash',
    )

    # Keep blockchain metadata protected
    readonly_fields = (
        'index',
        'timestamp',
        'previous_hash',
        'hash',
    )

    # Show editable payload only
    fields = (
        'index',
        'user',
        'data',          # editable -> simulate tampering
        'timestamp',
        'previous_hash',
        'hash',
    )

    def has_add_permission(self, request):
        return True      # allow adding blocks

    def has_change_permission(self, request, obj=None):
        return True      # ✅ enable editing for demo tampering

    def has_delete_permission(self, request, obj=None):
        return False     # still prevent deletion


# -----------------------------
# AUDIT LOG ADMIN (READ ONLY)
# -----------------------------
@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = (
        'action',
        'block',
        'user',
        'timestamp'
    )

    list_filter = (
        'action',
        'timestamp'
    )

    search_fields = (
        'message',
        'user__username'
    )

    ordering = ('-timestamp',)

    readonly_fields = (
        'user',
        'block',
        'action',
        'message',
        'timestamp'
    )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
