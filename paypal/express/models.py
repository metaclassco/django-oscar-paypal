import re

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from paypal import base


@python_2_unicode_compatible
class ExpressTransaction(base.ResponseModel):

    # The PayPal method and version used
    method = models.CharField(max_length=32)
    version = models.CharField(max_length=8)

    # Transaction details used in GetExpressCheckout
    amount = models.DecimalField(max_digits=12, decimal_places=2, null=True,
                                 blank=True)
    currency = models.CharField(max_length=8, null=True, blank=True)

    # Response params
    SUCCESS, SUCCESS_WITH_WARNING, FAILURE = 'Success', 'SuccessWithWarning', 'Failure'
    ack = models.CharField(max_length=32)

    correlation_id = models.CharField(max_length=32, null=True, blank=True)
    token = models.CharField(max_length=32, null=True, blank=True)

    error_code = models.CharField(max_length=32, null=True, blank=True)
    error_message = models.CharField(max_length=256, null=True, blank=True)

    class Meta:
        ordering = ('-date_created',)
        app_label = 'paypal'

    def save(self, *args, **kwargs):
        self.raw_request = re.sub(r'PWD=\d+&', 'PWD=XXXXXX&', self.raw_request)
        return super(ExpressTransaction, self).save(*args, **kwargs)

    @property
    def is_successful(self):
        return self.ack in (self.SUCCESS, self.SUCCESS_WITH_WARNING)

    def __str__(self):
        return 'method: %s: token: %s' % (
            self.method, self.token)


class ExpressCheckoutTransaction(models.Model):
    order_id = models.CharField(max_length=255)
    authorization_id = models.CharField(max_length=255, null=True, blank=True)
    capture_id = models.CharField(max_length=255, null=True, blank=True)
    refund_id = models.CharField(max_length=255, null=True, blank=True)
    payer_id = models.CharField(max_length=255, null=True, blank=True)

    email = models.EmailField(null=True, blank=True)

    amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    currency = models.CharField(max_length=8, null=True, blank=True)

    CREATED, SAVED, APPROVED, VOIDED, COMPLETED = 'CREATED', 'SAVED', 'APPROVED', 'VOIDED', 'COMPLETED'
    status = models.CharField(max_length=8)

    AUTHORIZE, CAPTURE = 'AUTHORIZE', 'CAPTURE'
    intent = models.CharField(max_length=9)

    address_full_name = models.CharField(max_length=255)
    address = models.TextField()

    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-date_created',)
        app_label = 'paypal'

    def __str__(self):
        if self.intent:
            return 'intent: {}, status: {}'

    @property
    def is_authorization(self):
        return self.intent == self.AUTHORIZE

    @property
    def is_completed(self):
        return self.status == self.COMPLETED
