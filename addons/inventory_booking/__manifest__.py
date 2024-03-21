{
    'name': 'Inventory booking',
    'version': '0.0.1',
    'category': 'Productivity',
    'description': "Inventory booking plugin",
    'website': 'https://erp.miem.hse.ru',
    'author': 'Antipov Vladislav',
    'depends': [
        'web',
        'website',
        'website_payment',
        'base',
        'purchase',
        'stock',
    ],
    'application': True,
    'data': [
        'data/ir_model_data.xml',
        'views/view_product_product.xml',
        'views/view_product_product_set.xml',
        'views/view_stock_rent.xml',
        'security/access_groups.xml',
        'security/ir.model.access.csv',
        'security/record_rules.xml',
    ],
    'assets': {
       'web.assets_frontend': [
           'inventory_booking/static/src/js/get_inventory_items.js',
       ],
    },
}
