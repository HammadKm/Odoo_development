# -*- coding: utf-8 -*-
{
    'name': "Reccuring Subscription",
    'version': '17.0.1.0.0',
    'depends': ['base','mail','product','crm','sale','account'],
    'author': "Author Name",
    'application': True,
    'category': 'Category',
    'description': """
    Creating a reccuring subscription module
    """,
    'data': [
        'security/recurring_user_groups.xml',
        'security/ir.model.access.csv',
        'data/recurring_subscription_sequence.xml',
        'data/subscription_product.xml',
        'data/scheduled_action_invoice.xml',
        'data/customer_email_template.xml',
        'view/inherited_partner_field.xml',
        'view/inherited_crm_view.xml',
        'view/recurring_subscription_view.xml',
        'view/recurring_subscription_credit.xml',
        'view/billing_schedule_view.xml',
        'wizard/recurring_subscription_report_wizard.xml',
        'wizard/recurring_subscription_credit_report_wizard.xml',
        'report/recurring_subscription_report.xml',
        'report/recurring_subscription_report_template.xml',
        'report/recurring_subscription_credit_report.xml',
        'report/recurring_subscription_credit_report_template.xml',
        'view/subscription_web_form_template.xml',
        'view/subscription_web_tree_template.xml',
        'view/subscription_credit_web_form_template.xml',
        'view/subscription_credit_snippet.xml',
        'view/snippet_view_template.xml',
        'view/subscription_snippet_form_template.xml',
        'view/recurring_subscription_website_menu.xml',
        'view/snippet_menu.xml',
        'view/recurring_subscription_menu.xml',


    ],
    'assets':{
        'web.assets_backend':[
            'reccuring_subscription/static/src/js/action_manager.js',
        ],
        'web.assets_frontend':[
            'reccuring_subscription/static/src/css/subscription_website.css',
            'reccuring_subscription/static/src/js/subscription_portal.js',
            'reccuring_subscription/static/src/xml/subscription_credit_snippet.xml',
            'reccuring_subscription/static/src/js/subscription_credit_snippet.js',
        ],
    },

    'license': 'OPL-1'
}