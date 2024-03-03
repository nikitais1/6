import logging
import smtplib

from django.conf import settings
from datetime import datetime, timezone, timedelta

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django.db.models import F
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django_apscheduler import util

from mailing.models import Mailing, MailingLog

logger = logging.getLogger(__name__)


def my_job():
    """Функция запуска рассылки"""
    now = datetime.now(timezone.utc)
    mailing_list = Mailing.objects.filter(sent_time__lte=now)
    for mailing in mailing_list:
        title = mailing.message.title
        message = mailing.message.message

        try:
            send_mail(
                subject=title,
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[client.client_email for client in mailing.mail_to.all()],
                fail_silently=False,
            )
            if mailing.periodicity == 'ONE_TIME':
                mailing.sent_time = None
                mailing.mailing_status = 'Finished'
            elif mailing.periodicity == 'DAILY':
                mailing.sent_time = F('sent_time') + timedelta(days=1)
                mailing.mailing_status = 'Running'
            elif mailing.periodicity == 'WEEKLY':
                mailing.sent_time = F('sent_time') + timedelta(days=7)
                mailing.mailing_status = 'Running'
            elif mailing.periodicity == 'MONTHLY':
                mailing.sent_time = F('sent_time') + timedelta(days=30)
                mailing.mailing_status = 'Running'
            mailing.save()

            status = 'Success'
            server_response = 'успешно'
        except smtplib.SMTPResponseException as error:
            status = 'Failed'
            server_response = str(error)

        finally:
            MailingLog.objects.create(mailing=mailing, status=status, server_response=server_response,
                                last_try_at=now)

# The `close_old_connections` decorator ensures that database connections, that have become
# unusable or are obsolete, are closed before and after your job has run. You should use it
# to wrap any jobs that you schedule that access the Django database in any way.
@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    """
    This job deletes APScheduler job execution entries older than `max_age` from the database.
    It helps to prevent the database from filling up with old historical records that are no
    longer useful.

    :param max_age: The maximum length of time to retain historical job execution records.
                    Defaults to 7 days.
    """
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            my_job,
            trigger=CronTrigger(second="*/10"),  # Every 10 seconds
            id="my_job",  # The `id` assigned to each job MUST be unique
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),  # Midnight on Monday, before start of the next work week.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")