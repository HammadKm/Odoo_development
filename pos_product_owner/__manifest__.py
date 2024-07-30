# -*- coding: utf-8 -*-

{
    'name': "POS Product owner",
    'version': '17.0.1.0.0',
    'depends': ['base','product','point_of_sale'],
    'author': "Author Name",
    'application': True,
    'category': 'Category',
    'description': """
    Adding product owner in pos line and recipt
    """,
    'data': [
        'views/product_product_form_view.xml',
    ],
    'license': 'OPL-1',
    'assets':{
        'point_of_sale._assets_pos': [
            'pos_product_owner/static/src/js/pos_product_owner.js',
            'pos_product_owner/static/src/xml/pos_product_owner.xml',

        ]
    },
}