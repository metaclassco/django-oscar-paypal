from django.utils.translation import gettext_lazy as _
from django.urls import path
from oscar.core.application import OscarDashboardConfig


class ExpressDashboardApplication(OscarDashboardConfig):
    name = "paypal.express.dashboard"
    label = "express_dashboard"
    namespace = "express_dashboard"
    verbose_name = _("Express dashboard")

    default_permissions = ["is_staff"]

    def get_urls(self):
        from . import views

        urlpatterns = [
            path('legacy/transactions/', views.LegacyTransactionListView.as_view(),
                 name='legacy-paypal-express-list'),
            path('legacy/transactions/<int:pk>/', views.LegacyTransactionDetailView.as_view(),
                 name='legacy-paypal-express-detail'),

            path('transactions/', views.TransactionListView.as_view(),
                 name='paypal-express-list'),
            path('transactions/<int:pk>/', views.TransactionDetailView.as_view(),
                 name='paypal-express-detail'),
        ]
        return self.post_process_urls(urlpatterns)
