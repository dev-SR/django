from django.contrib import admin

from .models import Conversation, Message


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('id', 'show_participants')
    autocomplete_fields = ('participants',)

    def show_participants(self, obj):
        return ', '.join([str(p) for p in obj.participants.all()])

    show_participants.short_description = 'Participants'


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'conversation',
        'sender',
        'content',
        'timestamp',
        'is_read',
    )
    list_filter = ('conversation', 'sender', 'timestamp', 'is_read')
