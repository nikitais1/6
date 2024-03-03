from django import forms

from mailing.models import Mailing, Message, Client



class StyleFormMixin:
    """
    Класс для стилизации форм
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class MailingForm(StyleFormMixin, forms.ModelForm):
    """
    Класс для создания и стилизации формы рассылки
    """

    class Meta:
        model = Mailing
        exclude = ('owner',)


class ManagerMailingForm(MailingForm):
    """
    Класс для создания формы рассылки для менеджера
    """

    class Meta:
        model = Mailing
        fields = ('status',)


class MessageForm(StyleFormMixin, forms.ModelForm):
    """
    Класс для создания и стилизации формы сообщения
    """

    class Meta:
        model = Message
        fields = '__all__'


class ClientForm(StyleFormMixin, forms.ModelForm):
    """
    Класс для создания и стилизации формы клиента для рассылки
    """
    class Meta:
        model = Client
        fields = '__all__'