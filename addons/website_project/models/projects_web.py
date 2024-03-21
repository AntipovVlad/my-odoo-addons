from odoo import models, fields


class WebProjects(models.Model):
    _inherit = 'project.project'

    display_on_website = fields.Boolean(string='If project can be displayed on website', default=False)
