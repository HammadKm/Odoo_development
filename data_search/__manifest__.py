# -*- coding: utf-8 -*-

{
    'name': "Data Search",
    'version': '17.0.1.0.0',
    'depends': ['base'],
    'author': "Author Name",
    'application': True,
    'category': 'Category',
    'description': """
    Settting a form view where one can search content from any searchable fields of any model.
    """,
    'data': [
        'security/ir.model.access.csv',
        'views/data_search_view.xml',
        'views/data_search_menu.xml',
    ],
    'license': 'OPL-1'
}