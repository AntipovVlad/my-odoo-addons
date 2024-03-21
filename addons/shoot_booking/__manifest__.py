{
    'name': 'Shoot booking',
    'version': '0.0.5',
    'category': 'Productivity',
    'description': "Shoot booking plugin",
    'website': 'https://erp.miem.hse.ru',
    'author': 'Antipov Vladislav',
    'depends': [
        'crm',
        'website',
        'web',
        'base',
        'hr',
        'zulip_integration'
    ],
    'application': True,
    'data': [
        'security/access_groups.xml',
        'security/ir.model.access.csv',
        'views/shoot_booking_crm_view.xml',
        'views/shoot_booking_views.xml',
    ],
    'assets': {
       'web.assets_frontend': [
           '/shoot_booking/static/src/js/get_slots.js',
       ],
    },
}
