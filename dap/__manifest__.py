# -*- coding: utf-8 -*-
{
    'name': "dap",

    'summary': """
        Module for the doctor appointment""",

    'description': """
        6073
    """,

    'author': "Silverdale",
    'website': "http://www.silverdaletech.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','vetapp','sale_management','report_xlsx','web'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'wizards/download.xml',
        'views/views.xml',
        'views/templates.xml',
        'views/mail_template.xml',
        'reports/report.xml',
        'reports/A_report_Excel.xml',
        'views/templates_controller.xml',
    ],
    # "images": ["js_framework_sample/static/description/icon.png"],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
