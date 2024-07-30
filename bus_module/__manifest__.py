# -*- coding: utf-8 -*-
{
    'name': 'Bus Module',
    'version': "1.0",
    'depends': ['web', 'bus'],
    'data': [
        'views/bus_test_action.xml'
    ],
    'assets': {
        'web.assets_backend': [
            "bus_module/static/src/js/bus_test.js",
            "bus_module/static/src/js/bus_test.xml"
        ],
    },
    'license': 'LGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
