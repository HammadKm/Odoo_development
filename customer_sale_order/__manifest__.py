# -*- coding: utf-8 -*-

{
    'name': "Customer Sale Order",
    'version': '17.0.1.0.0',
    'depends': ['base','contacts','sale'],
    'author': "Author Name",
    'application': True,
    'category': 'Category',
    'description': """
    Displaying the all sale order for the customer
    """,
    'data': [
        'view/inherited_customer_view.xml',
        'view/inherited_product_view.xml',
    ],
    'license': 'OPL-1'
}