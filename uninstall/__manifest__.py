# -*- coding: utf-8 -*-
{
    'name': "uninstall",

    'summary': """
        module for adding multiple modules uninstalling functionality""",

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
    'depends': ['base'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/uninstall_module.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
