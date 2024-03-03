from django.db import models
from dateutil.relativedelta import relativedelta
from users.models import User

NULLABLE = {'null': True, 'blank': True}


class Client(models.Model):
    email = models.EmailField(unique=True, verbose_name='Почта')
    fio = models.CharField(max_length=255, **NULLABLE, verbose_name='ФИО')
    comment = models.TextField(**NULLABLE, verbose_name='Комментарий')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def __str__(self):
        return f'{self.fio} - {self.email}'


class Message(models.Model):
    subject = models.CharField(max_length=255, verbose_name='Тема письма')
    content = models.TextField(verbose_name='Тело письма')

    class Meta:
        verbose_name = 'Письмо'
        verbose_name_plural = 'Письма'

    def __str__(self):
        return self.subject


class Period(models.IntegerChoices):
    ONE_TIME = 0, 'One-time'
    DAILY = 1, 'Daily'
    WEEKLY = 2, 'Weekly'
    MONTHLY = 3, 'Monthly'

    def as_relative_delta(self):
        match self:
            case self.DAILY:
                return relativedelta(days=1)
            case self.WEEKLY:
                return relativedelta(weeks=1)
            case self.MONTHLY:
                return relativedelta(months=1)
            case _:
                raise NotImplementedError


class Status(models.IntegerChoices):
    FINISHED = 1, 'Finished'
    CREATED = 2, 'Created'
    RUNNING = 3, 'Running'


class Mailing(models.Model):
    time_start = models.TimeField(verbose_name='Время начала рассылки')
    time_over = models.TimeField(verbose_name='Время окончания рассылки')
    period = models.PositiveSmallIntegerField(choices=Period.choices, verbose_name='Период рассылки')
    status = models.PositiveSmallIntegerField(choices=Status.choices, default=Status.CREATED,
                                              verbose_name='Статус рассылки'),
    clients = models.ManyToManyField(Client, verbose_name='Клиент')
    message = models.OneToOneField(Message, on_delete=models.PROTECT, related_name='mailing', verbose_name='Письмо')

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'

    def __str__(self):
        pass


class MailingLog(models.Model):
    SUCCESS = 0
    FAILED = 1
    STATUS_CHOICES = [(SUCCESS, 'Success'), (FAILED, 'Failed')]

    last_try_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время последней попытки')
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, verbose_name='Статус')
    server_response = models.TextField(**NULLABLE, verbose_name='Ответ сервера')
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, related_name='logs', verbose_name='Рассылка')

    class Meta:
        verbose_name = 'Лог'
        verbose_name_plural = 'Логи'

    def __str__(self):
        pass

# from django.core.mail import send_mail
# from django.core.exceptions import ValidationError
#
# try:  # Ваш код, который отправляет письмо
#
#     responce = send_mail('Тема письма', 'Текст письма.', 'отправитель@example.com', ['получатель@example.com'],
#                          fail_silently=False, )
#     MailingLog.objects.create(0, responce)
# except ValidationError as e:  # Обработка ошибок валидации
#     print(f"Ошибка валидации: {e}")
#
# except Exception as e:
#     print(f"Произошла ошибка при отправке письма: {e}")
#     MailingLog.objects.create(1, e, )
