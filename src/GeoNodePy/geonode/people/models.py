# -*- coding: UTF-8 -*-
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import signals
from django.utils.translation import ugettext as _

from django.contrib.auth.models import User

from idios.models import ProfileBase, create_profile

from geonode.core.models import COUNTRIES

from relationships.models import Relationship
from notification import models as notification

import logging
logger = logging.getLogger("geonode.people.models")

CONTACT_FIELDS = [
    "name",
    "organization",
    "position",
    "voice",
    "facsimile",
    "delivery_point",
    "city",
    "administrative_area",
    "postal_code",
    "country",
    "email",
    "role"
]


PROFILE_TYPES = (
    ('U', 'End User'),
    ('S', 'Supplier'),
    ('P', 'Provider'),
)

class Contact(ProfileBase):
    type = models.CharField(_('User Type'), max_length=1, choices=PROFILE_TYPES, null=True, blank=True, default='U')
    name = models.CharField(_('Individual Name'), max_length=255 )
    organization = models.CharField(_('Organisation Name'), max_length=255 )
    profile = models.TextField(_('Profile'), null=True, blank=True)
    position = models.CharField(_('Position Name'), max_length=255, blank=True, null=True)
    voice = models.CharField(_('Contact number'), max_length=255)
    fax = models.CharField(_('Facsimile'),  max_length=255, blank=True, null=True)
    delivery = models.CharField(_('Delivery Point'), max_length=255, blank=True, null=True)
    city = models.CharField(_('City'), max_length=255, blank=True, null=True)
    area = models.CharField(_('Administrative Area'), max_length=255, blank=True, null=True)
    zipcode = models.CharField(_('Postal Code'), max_length=255, blank=True, null=True)
    country = models.CharField(choices=COUNTRIES, max_length=3, blank=True, null=True)
    email = models.EmailField()

    def clean(self):
        # the specification says that either name or organization should be provided
        valid_name = (self.name != None and self.name != '')
        valid_organization = (self.organization != None and self.organization !='')
        if not (valid_name or valid_organization):
            raise ValidationError('Either name or organization should be provided')

    def __unicode__(self):
        return u"%s (%s)" % (self.name, self.organization)

def create_user_profile(instance, sender, created, **kwargs):
    try:
        profile = Contact.objects.get(user=instance)
    except Contact.DoesNotExist:
        profile = Contact(user=instance)
        profile.name = instance.username
        profile.save()

# Connect notice creation to new following relationships.
def notify_on_follow(instance, sender, **kwargs):
    """
    Notify the followed user that they have a new follower.

    This handler is present since the relationhip model itself doesn't send notifications.
    """
    if instance.status.verb == "follow":
        notification.send([instance.to_user],
                        "user_followed",
                        {"from_user": instance.from_user, "user_url": instance.from_user.get_absolute_url()},
                        on_site=True
        )
        logger.info("Notification sent from {0} to {1}".format(instance.to_user, instance.from_user))

signals.post_save.connect(notify_on_follow, sender=Relationship)

# Remove the idios create_profile handler, which interferes with ours.
signals.post_save.disconnect(create_profile, sender=User)
signals.post_save.connect(create_user_profile, sender=User)
