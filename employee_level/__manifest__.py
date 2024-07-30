# -*- coding: utf-8 -*-

{
    'name': "Employee Level",
    'version': '17.0.1.0.0',
    'depends': ['base','hr'],
    'author': "Author Name",
    'application': True,
    'category': 'Category',
    'description': """
    Adding Employee level and salary
    """,
    'data': [
        'security/ir.model.access.csv',
        'view/employee_level_tree_view.xml',
        'view/inherited_employee_view.xml',
    ],
    'license': 'OPL-1'
}