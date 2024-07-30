# -*- coding: utf-8 -*-

{
    'name': "POS discount limit",
    'version': '17.0.1.0.0',
    'depends': ['base','point_of_sale'],
    'author': "Author Name",
    'application': True,
    'category': 'Category',
    'description': """
    Adding session wise discount limit in Pos
    """,
    'data': [
        'views/pos_config_settings_view.xml',
        'views/pos_session_view.xml',
    ],
    'license': 'OPL-1',
    'assets':{
        'point_of_sale._assets_pos': [
            'pos_discount_limit/static/src/js/pos_discount_limt.js'
        ]
    },
}