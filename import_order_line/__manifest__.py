# -*- coding: utf-8 -*-

{
    'name': "Import Order Line",
    'version': '17.0.1.0.0',
    'depends': ['base','sale'],
    'author': "Author Name",
    'application': True,
    'category': 'Category',
    'description': """
    Import Order lines into sales from xlx sheet
    """,
    'data': [
        'security/ir.model.access.csv',
        'wizard/import_wizard_view.xml',
        'view/inherited_sales_order_line_view.xml',
    ],
    'license': 'OPL-1'
}