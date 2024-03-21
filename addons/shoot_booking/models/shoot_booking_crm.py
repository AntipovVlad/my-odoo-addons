from odoo.exceptions import AccessError, ValidationError

from odoo import api, fields, models

DEFAULT_SHOOT_BOOKING_STAGES = [
    'Web Request',
    'In Discussion',
    'In Process',
    'Done',
    'Lost'
]


class ShootBookingCRMLead(models.Model):
    _inherit = 'crm.lead'

    shoot_slot_id = fields.Many2one(comodel_name='calendar.shoot_booking',
                                    string='Free shoot slot',
                                    domain="[('crm_pipeline_id.id', '=', 'team_id')]", default=None)
    assigned_to_id = fields.Many2one(comodel_name='hr.employee', string='Assigned person', default=None)

    slot_type = fields.Selection(selection=[('direct', 'Режиссируемая'),
                                            ('not direct', 'Нережиссируемая'),
                                            ('none', '')],
                                 string='Type of shoot',
                                 default='none')

    is_slot_booking = fields.Boolean(related='team_id.is_slot_booking')
    notification_bot = fields.Many2one(related='team_id.notification_bot')

    @api.model
    def create(self, vals_list):
        if vals_list.get('shoot_slot_id') and vals_list.get('slot_type') == 'not direct':
            raise ValidationError('Impossible variable combination')

        if vals_list.get('shoot_slot_id'):
            record = self.env['calendar.shoot_booking'].search([('id', '=', vals_list['shoot_slot_id'])])[0]
            if record['current_available_slots'] > 0:
                record.update({'current_available_slots': record['current_available_slots'] - 1})
            else:
                raise ValidationError('Prohibited slot')

            vals_list['stage_id'] = self.env['crm.stage'].search(['&', ('team_id.id', '=', vals_list['team_id']), ('name', '=', 'Web Request')])[0].id

        return super(ShootBookingCRMLead, self).create(vals_list)

    def write(self, vals):
        if vals.get('assigned_to_id') and self.notification_bot is not None:
            email = self.env['hr.employee'].search([('id', '=', vals.get('assigned_to_id'))])[0]['work_email']
            self.notification_bot.bot_reference.zulip_bot_send_message_private([email], 'You were assigned to shoot')

        return super(ShootBookingCRMLead, self).write(vals)


class ShootBookingCRMTeam(models.Model):
    _inherit = 'crm.team'

    is_slot_booking = fields.Boolean(string='Calendar shoot booking', default=False)
    notification_bot = fields.Many2one(comodel_name='bots.bots',
                                       string='Bot for sending notifications to users',
                                       default=False)

    def _add_default_shoot_booking_stages(self, team_id: str):
        for i, stage_name in enumerate(globals().get('DEFAULT_SHOOT_BOOKING_STAGES')):
            stage_existence = self.env['crm.stage'].search(['&', ('name', '=', stage_name), ('team_id', '=', team_id)])
            if len(stage_existence) == 0:
                self.env['crm.stage'].create({'name': stage_name, 'sequence': i, 'team_id': team_id})

    @api.model
    def create(self, vals_list):
        team_id = super(ShootBookingCRMTeam, self).create(vals_list)
        if vals_list.get('is_slot_booking'):
            self._add_default_shoot_booking_stages(team_id.id)

        return team_id

    def write(self, vals):
        if vals.get('is_slot_booking'):
            self._add_default_shoot_booking_stages(self.id)

        return super(ShootBookingCRMTeam, self).write(vals)
