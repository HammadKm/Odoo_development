# -*- coding: utf-8 -*-

{
    'name': "Payment PayU",
    'version': '17.0.1.0.0',
    'depends': ['payment'],
    'author': "Author Name",
    'application': True,
    'category': 'Category',
    'description': """
    Integrating  payU payment gateway with odoo
    """,
    'data': [
        'data/payment_method_payu.xml',
        'views/payment_payu_template.xml',
        'views/payment_provider_views.xml',
        'data/payu_payment.xml',
    ],
    # 'pre_init_hook': 'pre_init_hook',
    'post_init_hook': 'post_init_hook',
    'uninstall_hook': 'uninstall_hook',
    'license': 'OPL-1',
}