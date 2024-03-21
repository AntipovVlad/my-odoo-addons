from odoo import models, fields, api
from odoo.exceptions import ValidationError

from random import randint

CONSTRAIN_FIELDS = [
    'personnel_trainee_number',
    'personnel_employee_number',
    'readiness_miem_presentation',
    'readiness_miem_experts',
    'readiness_miem_final',
    'rid_perspectives',
    'rid_exists',
    'rid_plan',
    'science_pub_perspectives',
    'science_pub_exists',
    'science_pub_plan',
    'media_perspectives',
    'media_exists',
    'media_plan',
    'integration_perspectives',
    'integration_exists',
    'integration_plan',
    'marketing_web',
    'marketing_paper',
    'marketing_presentation',
    'marketing_demo',
    'product_readiness_science',
    'product_readiness_engineering',
    'product_readiness_technology',
    'product_readiness_programming',
    'product_readiness_operation',
    'product_readiness_marketing',
    'product_readiness_stage',
    'product_readiness_risks',
]


class ProjectType(models.Model):
    _inherit = 'project.tags'

    @api.model
    def _add_new_media_center_tags(self):
        tags = ['Стартап', 'Эксплуат', 'ПО', 'АП']
        for tag in tags:
            self.create({'name': tag, 'color': randint(0, 11)})


class ProjectDevDirection(models.Model):
    _name = 'project.direction'
    _description = 'Project development direction'

    name = fields.Char(string='Name', required=True)


class ProjectsKPI(models.Model):
    _inherit = 'project.project'

    project_number_report = fields.Integer(string='Summary / Project / Number',
                                           compute='_set_report_project_number',
                                           store=True)
    project_status = fields.Char(string='Summary / Project / Status',
                                 default='',
                                 compute='_set_project_status',
                                 store=True)
    development_direction = fields.Many2one(comodel_name='project.direction',
                                            string='Summary / Project / Development Direction')
    project_type = fields.Char(string='Summary / Project / Type',
                               default='',
                               compute='_set_project_type',
                               store=True)

    personnel_leader_report = fields.Many2one(comodel_name='res.users',
                                              string='Summary / Personnel / Leader',
                                              compute='_set_report_team_leader', )
    personnel_trainee_number = fields.Integer(string='Summary / Personnel / Trainees')
    personnel_employee_number = fields.Integer(string='Summary / Personnel / Employees')

    readiness_miem_presentation = fields.Integer(string='Summary / Readiness MIEM / Middle presentation')
    readiness_miem_experts = fields.Integer(string='Summary / Readiness MIEM / Expert control')
    readiness_miem_final = fields.Integer(string='Summary / Readiness MIEM / Final presentation')

    rid_perspectives = fields.Integer(string='Summary / RID / Perspectives')
    rid_exists = fields.Integer(string='Summary / RID / Exists')
    rid_plan = fields.Integer(string='Summary / RID / Plan')

    science_pub_perspectives = fields.Integer(string='Summary / Science publishing / Perspectives')
    science_pub_exists = fields.Integer(string='Summary / Science publishing / Exists')
    science_pub_plan = fields.Integer(string='Summary / Science publishing / Plan')

    media_perspectives = fields.Integer(string='Summary / Media publishing / Perspectives')
    media_exists = fields.Integer(string='Summary / Media publishing / Exists')
    media_plan = fields.Integer(string='Summary / Media publishing / Plan')

    integration_perspectives = fields.Integer(string='Summary / Integration / Perspectives')
    integration_exists = fields.Integer(string='Summary / Integration / Exists')
    integration_plan = fields.Integer(string='Summary / Integration / Plan')

    marketing_web = fields.Integer(string='Summary / Marketing / Web')
    marketing_paper = fields.Integer(string='Summary / Marketing / Paper')
    marketing_presentation = fields.Integer(string='Summary / Marketing / Presentation')
    marketing_demo = fields.Integer(string='Summary / Marketing / Demo')

    product_readiness_science = fields.Integer(string='Summary / Product readiness / Science')
    product_readiness_engineering = fields.Integer(string='Summary / Product readiness / Engineering')
    product_readiness_technology = fields.Integer(string='Summary / Product readiness / Technology')
    product_readiness_programming = fields.Integer(string='Summary / Product readiness / Programming')
    product_readiness_operation = fields.Integer(string='Summary / Product readiness / Operation')
    product_readiness_marketing = fields.Integer(string='Summary / Product readiness / Marketing')
    product_readiness_stage = fields.Integer(string='Summary / Product readiness / Stage')
    product_readiness_risks = fields.Integer(string='Summary / Product readiness / Risks')

    currency_id = fields.Many2one(comodel_name='res.currency',
                                  string="Currency",
                                  related='company_id.currency_id',
                                  default=lambda self: self.env.user.company_id.currency_id.id)
    budget_investments = fields.Monetary(string='Summary / Budget / Investments')
    budget_income = fields.Monetary(string='Summary / Budget / Income')
    budget_fot = fields.Monetary(string='Summary / Budget / FOT')
    budget_materials = fields.Monetary(string='Summary / Budget / Materials')
    budget_services = fields.Monetary(string='Summary / Budget / Services')
    budget_balance = fields.Monetary(string='Summary / Budget / Balance')

    @api.depends('tag_ids')
    def _set_project_type(self):
        for rec in self:
            if not rec.tag_ids:
                rec.project_type = ''
            else:
                rec.project_type = rec.tag_ids[0].name

    @api.depends('last_update_status')
    def _set_project_status(self):
        for rec in self:
            rec.project_status = dict(self._fields['last_update_status'].selection).get(rec.last_update_status)

    @api.depends('x_project_number')
    def _set_report_project_number(self):
        for rec in self:
            rec.project_number_report = rec.x_project_number

    @api.depends('user_id')
    def _set_report_team_leader(self):
        for rec in self:
            rec.personnel_leader_report = rec.user_id

    @api.constrains(*globals().get('CONSTRAIN_FIELDS'))
    def _check_if_positive_number(self):
        for rec in self:
            if any([rec[k] < 0 for k in globals().get('CONSTRAIN_FIELDS')]):
                raise ValidationError('Incorrect field data!')

    def get_report_field(self) -> dict:
        emp = -1
        sheets = {}
        for rec in self._fields:
            if len(hierarchy := self._fields[rec].string.split(' / ')) > 1:
                headers = hierarchy[1:]

                if sheets.get(hierarchy[0]):
                    if len(headers) == 1:
                        sheets[hierarchy[0]][emp] = headers
                        emp -= 1
                    else:
                        if sheets[hierarchy[0]].get(headers[0]):
                            sheets[hierarchy[0]][headers[0]].append(headers[1])
                        else:
                            sheets[hierarchy[0]][headers[0]] = headers[1:]
                else:
                    if len(headers) == 1:
                        sheets[hierarchy[0]] = {emp: headers}
                        emp -= 1
                    else:
                        sheets[hierarchy[0]] = {headers[0]: headers[1:]}
        return sheets

    def get_report_lines(self) -> tuple:
        r_lines = []
        for name, field in self._fields.items():
            if len(field.string.split(' / ')) > 1:
                line = [record[name] for record in self.search([])]
                if isinstance(field, fields.Selection):
                    line = list(map(lambda x: '' if not x else dict(field.selection)[x], line))
                if isinstance(field, (fields.One2many, fields.Many2one, fields.Many2many)):
                    line = list(map(lambda x: '' if not x else x.name, line))

                r_lines.append(line)

        return tuple(zip(*r_lines))
