# -*- coding: utf-8 -*-

{
    'name': "Material Request",
    'version': '17.0.1.0.0',
    'depends': ['base','mail','product','stock'],
    'author': "Author Name",
    'application': True,
    'category': 'Category',
    'description': """
    Request for the materials
    """,
    'data': [
        'security/material_request_users.xml',
        'security/ir.model.access.csv',
        'views/material_request_view.xml',
        'views/material_request_website_template.xml',
        'views/material_request_thank_template.xml',
        'data/material_request_sequence.xml',
        'data/material_response_email_template.xml',
        'views/material_request_website_menu.xml',
        'views/material_request_menu.xml',
    ],
    'assets':{
        'web.assets_frontend':[
            'material_request/static/src/js/material_request.js',
        ],
    },
    'license': 'OPL-1'
}