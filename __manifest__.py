{
    'name': 'Czech Payment Integration',
    'version': '1.0',
    'category': 'Accounting',
    'summary': 'Integrate local Czech payment providers like GoPay and PayU Czech into Odoo',
    'author': 'Your Name',
    'depends': ['account', 'payment'],
    'data': [
        'views/payment_provider_views.xml',
        'views/config_settings_view.xml',  # Add the settings view
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'application': False,
}
