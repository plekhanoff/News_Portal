from os import link
from typing import List

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.template.defaultfilters import title
from django.template.loader import render_to_string




class PostCategory:
    pass


@receiver(m2m_changed, sender=PostCategory)
def notify_about_new_post(instance, category=None, **kwargs):
    if kwargs['action'] == 'post_add':
        categories = instance.category.all()
        subscribers: List[str] = []
        for categories in categories:
            subscribers += category.subscribers.all()

        subscribers = [s.email for s in subscribers]
        send_notifications(instance.preview(), instance.pk, instance.title, subscribers)


def send_notifications(preview, pk, title, subscribers, ):
    from prj.prj.settings import SITE_URL
    html_content = render_to_string('post_created_email.html', {'text': preview,
                                                                link: f'{SITE_URL / title / {pk} }'})

    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers, )

    msg.attach_alternative(msg, 'text/html')
    msg.send()

