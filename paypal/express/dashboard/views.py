from django.conf import settings
from django.views import generic

from paypal.express import models


class LegacyTransactionListView(generic.ListView):
    model = models.ExpressTransaction
    template_name = 'paypal/express/dashboard/legacy/transaction_list.html'
    context_object_name = 'transactions'


class LegacyTransactionDetailView(generic.DetailView):
    model = models.ExpressTransaction
    template_name = 'paypal/express/dashboard/legacy/transaction_detail.html'
    context_object_name = 'txn'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['show_form_buttons'] = getattr(
            settings, 'PAYPAL_PAYFLOW_DASHBOARD_FORMS', True)
        return ctx


class TransactionListView(generic.ListView):
    model = models.ExpressCheckoutTransaction
    template_name = 'paypal/express/dashboard/transaction_list.html'
    context_object_name = 'transactions'


class TransactionDetailView(generic.DetailView):
    model = models.ExpressCheckoutTransaction
    template_name = 'paypal/express/dashboard/transaction_detail.html'
    context_object_name = 'txn'
