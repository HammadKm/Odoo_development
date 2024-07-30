# -*- coding: utf-8 -*-

{
    'name': "Systray icon weather",
    'version': '17.0.1.0.0',
    'depends': ['base','base_setup'],
    'author': "Author Name",
    'application': True,
    'category': 'Category',
    'description': """
    Adding button in systray to show the current weather
    """,
    'data': [
        'views/res_config_settings_views.xml',
    ],
    'license': 'OPL-1',
    'assets':{
        'web.assets_backend': [
            'systray_icon_weather/static/src/js/systray_icon.js',
            'systray_icon_weather/static/src/xml/systray_icon.xml',
   ],
    },
}