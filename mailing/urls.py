from django.urls import path

from mailing.apps import MailingConfig
from mailing.views import ClientCreateView, ClientDetailView, ClientListView, ClientUpdateView, ClientDeleteView, \
    MessageCreateView, MessageListView, MessageDetailView, MessageUpdateView, MessageDeleteView, MailingCreateView, \
    MailingListView, MailingDetailView, MailingUpdateView, MailingDeleteView, MailingLogListView, \
    index

app_name = MailingConfig.name

urlpatterns = [
    path('', index, name='index'),

    path('client/create/', ClientCreateView.as_view(), name='create_client'),
    path('client/view/', ClientListView.as_view(), name='view_client'),
    path('client/view/<int:pk>/', ClientDetailView.as_view(), name='single_view_client'),
    path('client/update/<int:pk>/', ClientUpdateView.as_view(), name='update_client'),
    path('client/delete/<int:pk>/', ClientDeleteView.as_view(), name='delete_client'),

    path('message/create/', MessageCreateView.as_view(), name='create_message'),
    path('message/view/', MessageListView.as_view(), name='view_message'),
    path('message/view/<int:pk>/', MessageDetailView.as_view(), name='single_view_message'),
    path('message/update/<int:pk>/', MessageUpdateView.as_view(), name='update_message'),
    path('message/delete/<int:pk>/', MessageDeleteView.as_view(), name='delete_message'),

    path('mailing/create/', MailingCreateView.as_view(), name='create_mailing'),
    path('mailing/view/', MailingListView.as_view(), name='view_mailing'),
    path('mailing/view/<int:pk>/', MailingDetailView.as_view(), name='single_view_mailing'),
    path('mailing/update/<int:pk>/', MailingUpdateView.as_view(), name='update_mailing'),
    path('mailing/delete/<int:pk>/', MailingDeleteView.as_view(), name='delete_mailing'),

    path('mailinglog/view/', MailingLogListView.as_view(), name='view_mailinglog'),
]