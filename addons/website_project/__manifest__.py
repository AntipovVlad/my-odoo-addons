{
    'name': 'Website project',
    'version': '0.0.1',
    'category': 'Productivity',
    'description': "Web access rules plugin",
    'website': 'https://erp.miem.hse.ru',
    'author': 'Antipov Vladislav',
    'depends': [
        'base',
        'website',
        'project',
    ],
    'application': True,
    'data': [
        'views/website_project.xml',
        'views/view_projects_website.xml',
        'data/data.xml',
    ],
}
