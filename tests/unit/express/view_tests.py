from decimal import Decimal as D
from unittest.mock import Mock, patch
from urllib.parse import urlencode

from django.test import TestCase
from django.urls import reverse
from oscar.apps.basket.models import Basket
from oscar.apps.checkout.utils import CheckoutSessionData
from oscar.apps.order.models import Order
from oscar.test.factories import create_product

from paypalhttp.http_error import HttpError
from paypalhttp.http_response import construct_object

from tests.shipping.methods import SecondClassRecorded
from .mocked_data import capture_order_result_data, get_order_result_data


class BasketMixin:

    def add_product_to_basket(self, price=D('100.00')):
        product = create_product(price=price, num_in_stock=1)
        url = reverse('basket:add', kwargs={'pk': product.pk})
        self.client.post(url, {'quantity': 1})


class EdgeCaseTests(BasketMixin, TestCase):

    def setUp(self):
        super().setUp()
        self.url = reverse('paypal-redirect')

    def test_empty_basket_shows_error(self):
        response = self.client.get(self.url)
        assert reverse('basket:summary') == response.url

    def test_missing_shipping_address(self):
        from paypal.express.views import RedirectToPayPalView
        with patch.object(RedirectToPayPalView, 'as_payment_method') as as_payment_method:
            as_payment_method.return_value = True

            self.add_product_to_basket()
            response = self.client.get(self.url)
            assert reverse('checkout:shipping-address') == response.url

    def test_missing_shipping_method(self):
        from paypal.express.views import RedirectToPayPalView

        with patch.object(RedirectToPayPalView, 'as_payment_method') as as_payment_method:
            with patch.object(RedirectToPayPalView, 'get_shipping_address') as get_shipping_address:
                with patch.object(RedirectToPayPalView, 'get_shipping_method') as get_shipping_method:

                    as_payment_method.return_value = True
                    get_shipping_address.return_value = Mock()
                    get_shipping_method.return_value = None

                    self.add_product_to_basket()
                    response = self.client.get(self.url)
                    assert reverse('checkout:shipping-method') == response.url


class RedirectToPayPalTests(BasketMixin, TestCase):

    def setUp(self):
        super().setUp()
        self.url = reverse('paypal-redirect')

    def test_nonempty_basket_redirects_to_paypal(self):
        order_approve_url = 'https://www.sandbox.paypal.com/checkoutnow?token=9W253214FB287071X'

        with patch('paypal.express.gateway_new.PaymentProcessor.create_order') as create_order:
            create_order.return_value = order_approve_url

            self.add_product_to_basket()
            response = self.client.get(self.url)
            assert response.url == order_approve_url

    def test_paypal_error_redirects_to_basket(self):
        with patch('paypal.express.gateway_new.PaymentProcessor.create_order') as create_order:
            create_order.side_effect = HttpError(message='Error message', status_code=404, headers=None)

            self.add_product_to_basket()
            response = self.client.get(self.url)
            assert reverse('basket:summary') == response.url


class PreviewOrderTests(BasketMixin, TestCase):
    fixtures = ['countries.json']

    def setUp(self):
        super().setUp()

        self.add_product_to_basket(price=D('9.99'))
        basket = Basket.objects.all().first()
        basket.freeze()

        url = reverse('paypal-success-response', kwargs={'basket_id': basket.id})
        query_string = urlencode({'PayerID': '0000000000001', 'token': '4MW805572N795704B'})
        self.url_with_query_string = '{}?{}'.format(url, query_string)

        # Imitate selecting of shipping method in `form_valid` method of `ShippingMethodView`
        session = self.client.session
        session[CheckoutSessionData.SESSION_KEY] = {'shipping': {'method_code': SecondClassRecorded.code}}
        session.save()

    def test_context(self):
        with patch('paypal.express.gateway_new.PaymentProcessor.get_order') as get_order:
            get_order.return_value = construct_object('Result', get_order_result_data)

            response = self.client.get(self.url_with_query_string, follow=True)

            context = response.context
            assert D('19.99') == context['paypal_amount']
            assert 'Royal Mail Signed For™ 2nd Class' == context['shipping_method'].name
            assert 'uk_rm_2ndrecorded' == context['shipping_method'].code

            keys = ('shipping_address', 'shipping_method', 'payer_id', 'token', 'paypal_user_email', 'paypal_amount')
            for k in keys:
                assert k in context, '{} not in context'.format(k)

    def test_paypal_error_redirects_to_basket(self):
        self.add_product_to_basket(price=D('9.99'))
        basket = Basket.objects.all().first()
        basket.freeze()

        with patch('paypal.express.gateway_new.PaymentProcessor.get_order') as get_order:
            get_order.side_effect = HttpError(message='Error message', status_code=404, headers=None)

            response = self.client.get(self.url_with_query_string)
            assert reverse('basket:summary') == response.url


class SubmitOrderTests(BasketMixin, TestCase):
    fixtures = ['countries.json']

    def setUp(self):
        super().setUp()

        self.add_product_to_basket(price=D('9.99'))
        basket = Basket.objects.all().first()
        basket.freeze()

        self.url = reverse('paypal-place-order', kwargs={'basket_id': basket.id})
        self.payload = {
            'action': 'place_order',
            'payer_id': '0000000000001',
            'token': '4MW805572N795704B',
        }

        # Imitate selecting of shipping method in `form_valid` method of `ShippingMethodView`
        session = self.client.session
        session[CheckoutSessionData.SESSION_KEY] = {'shipping': {'method_code': SecondClassRecorded.code}}
        session.save()

    def test_created_order(self):
        with patch('paypal.express.gateway_new.PaymentProcessor.get_order') as get_order:
            with patch('paypal.express.gateway_new.PaymentProcessor.capture_order') as capture_order:

                get_order.return_value = construct_object('Result', get_order_result_data)
                capture_order.return_value = construct_object('Result', capture_order_result_data)

                self.client.post(self.url, self.payload)

                order = Order.objects.all().first()
                assert order.total_incl_tax == D('9.99')
                assert order.guest_email == 'sherlock.holmes@example.com'

                address = order.shipping_address
                assert address.line1 == '221B Baker Street'
                assert address.line4 == 'London'
                assert address.country.iso_3166_1_a2 == 'GB'
                assert address.postcode == 'WC2N 5DU'

    def test_paypal_error_redirects_to_basket(self):
        with patch('paypal.express.gateway_new.PaymentProcessor.get_order') as get_order:
            with patch('paypal.express.gateway_new.PaymentProcessor.capture_order') as capture_order:

                get_order.return_value = construct_object('Result', get_order_result_data)
                capture_order.side_effect = HttpError(message='Error message', status_code=404, headers=None)

                response = self.client.post(self.url, self.payload)
                assert reverse('basket:summary') == response.url
