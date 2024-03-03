from django.contrib import admin

from mailing.models import Client, Message, Mailing, MailingLog


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('email', 'fio', 'comment', 'user',)
    list_filter = ('email',)
    search_fields = ('email', 'fio',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('subject', 'content',)
    list_filter = ('subject',)
    search_fields = ('subject',)


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('time_start', 'time_over', 'period', 'status',)
    list_filter = ('time_start', 'time_over', 'period',)
    search_fields = ('time_start', 'time_over',)


@admin.register(MailingLog)
class LogsAdmin(admin.ModelAdmin):
    list_display = ('mailing', 'status')
