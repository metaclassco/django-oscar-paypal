get_order_result_data = {
    'create_time': '2019-12-27T16:39:20Z',
    'id': '4MW805572N795704B',
    'intent': 'CAPTURE',
    'links': [
        {
            'href': 'https://api.sandbox.paypal.com/v2/checkout/orders/4MW805572N795704B',
            'method': 'GET',
            'rel': 'self'
        },
        {
            'href': 'https://api.sandbox.paypal.com/v2/checkout/orders/4MW805572N795704B/capture',
            'method': 'POST',
            'rel': 'capture'
        }
    ],
    'payer': {
        'address': {
            'country_code': 'GB'
        },
        'email_address': 'sherlock.holmes@example.com',
        'name': {
            'given_name': 'Sherlock',
            'surname': 'Holmes'
        },
        'payer_id': '0000000000001'
    },
    'purchase_units': [
        {
            'amount': {
                'breakdown': {
                    'item_total': {
                        'currency_code': 'GBP',
                        'value': '9.99'
                    },
                    'shipping': {
                        'currency_code': 'GBP',
                        'value': '10.00'
                    }
                },
                'currency_code': 'GBP',
                'value': '19.99'
            },
            'items': [
                {
                    'category': 'PHYSICAL_GOODS',
                    'description': (
                        "The Shellcoder's Handbook shows you how to: Non-Find out where security holes come from "
                        "and how to close them so they neve..."
                    ),
                    'name': "The shellcoder's handbook",
                    'quantity': '1',
                    'sku': '9780764544682',
                    'unit_amount': {
                        'currency_code': 'GBP',
                        'value': '9.99'
                    }
                }
            ],
            'payee': {
                'email_address': 'seller@example.com',
                'merchant_id': '1234567890111'
            },
            'reference_id': 'default',
            'shipping': {
                'address': {
                    'address_line_1': '221B Baker Street',
                    'admin_area_2': 'London',
                    'country_code': 'GB',
                    'postal_code': 'WC2N 5DU'
                },
                'name': {
                    'full_name': 'Sherlock Holmes'
                }
            }
        }
    ],
    'status': 'APPROVED'
}


capture_order_result_data = {
    'id': '4MW805572N795704B',
    'links': [
        {
            'href': 'https://api.sandbox.paypal.com/v2/checkout/orders/4MW805572N795704B',
            'method': 'GET',
            'rel': 'self'
        }
    ],
    'payer': {
        'address': {
            'country_code': 'GB'
        },
        'email_address': 'sherlock.holmes@example.com',
        'name': {
            'given_name': 'Sherlock',
            'surname': 'Holmes'
        },
        'payer_id': '0000000000001'
    },
    'purchase_units': [
        {
            'payments': {
                'captures': [
                    {
                        'amount': {
                            'currency_code': 'GBP',
                            'value': '19.99'
                        },
                        'create_time': '2019-12-30T18:31:01Z',
                        'final_capture': True,
                        'id': '2D6171889X1782919',
                        'links': [
                            {
                                'href': 'https://api.sandbox.paypal.com/v2/payments/captures/2D6171889X1782919',
                                'method': 'GET',
                                'rel': 'self'
                            },
                            {
                                'href': 'https://api.sandbox.paypal.com/v2/payments/captures/2D6171889X1782919/refund',
                                'method': 'POST',
                                'rel': 'refund'
                            },
                            {
                                'href': 'https://api.sandbox.paypal.com/v2/checkout/orders/4MW805572N795704B',
                                'method': 'GET',
                                'rel': 'up'
                            }
                        ],
                        'seller_protection': {
                            'dispute_categories': [
                                'ITEM_NOT_RECEIVED',
                                'UNAUTHORIZED_TRANSACTION'
                            ],
                            'status': 'ELIGIBLE'
                        },
                        'status': 'PENDING',
                        'status_details': {
                            'reason': 'RECEIVING_PREFERENCE_MANDATES_MANUAL_ACTION'
                        },
                        'update_time': '2019-12-30T18:31:01Z'
                    }
                ]
            },
            'reference_id': 'default',
            'shipping': {
                'address': {
                    'address_line_1': '221B Baker Street',
                    'admin_area_2': 'London',
                    'country_code': 'GB',
                    'postal_code': 'WC2N 5DU'
                },
                'name': {
                    'full_name': 'Sherlock Holmes'
                }
            }
        }
    ],
    'status': 'COMPLETED'
}
