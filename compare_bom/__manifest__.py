# -*- coding: utf-8 -*-

{
    'name': "BOM Compare",
    'version': '17.0.1.0.0',
    'depends': ['base','mrp','web'],
    'author': "Author Name",
    'application': True,
    'category': 'Category',
    'description': """
    Comparing BOM of same products and show which is more profitable.
    """,
    'data': [
        'security/ir.model.access.csv',
        'wizard/compare_bom_view.xml',
        'report/compare_bom_report.xml',
        'report/compare_bom_report_template.xml',
        'views/mrp_bom_list_view.xml',

    ],
    'license': 'OPL-1',
    'assets':{
        'web.assets_backend': [
            'compare_bom/static/src/js/bom_compare_button.js',
            'compare_bom/static/src/xml/bom_list_tree_button.xml',
        ],
    },
}