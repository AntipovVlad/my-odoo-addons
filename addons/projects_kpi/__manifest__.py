{
    'name': 'Project KPI',
    'version': '0.0.2',
    'category': 'Productivity',
    'description': "Project KPI plugin",
    'website': 'https://erp.miem.hse.ru',
    'author': 'Antipov Vladislav',
    'depends': [
        'web',
        'base',
        'project',
    ],
    'application': True,
    'data': [
        'views/view_project_project_form.xml',
        'views/view_project_project_report.xml',
        'views/view_project_project_tree.xml',
        'data/add_dev_directions.xml',
        'data/add_new_tags.xml',
        'security/ir.model.access.csv',
    ],
}
