from odoo import fields, models, api
from odoo.exceptions import ValidationError


class ShootBooking(models.Model):
    _name = 'calendar.shoot_booking'
    _description = 'Free slots for shoot'

    event_date = fields.Date(string='Date of shoot', required=True)
    event_date_time = fields.Datetime(string='Date and time of shoot', required=True)
    current_available_slots = fields.Integer(string='Number of free slots', required=True)
    max_available_slots = fields.Integer(string='Max day free slots', requred=True)
    is_inside_slot = fields.Boolean(string='Is HSE slot', default=False)

    crm_pipeline_id = fields.Many2one(comodel_name='crm.team', string='Media Center team',
                                      domain='[("user_id", "=", uid)]', required=True, index=True)

    @api.constrains('current_available_slots', 'event_date')
    def _validate_current_available_slots(self):
        for record in self:
            if record.event_date != record.event_date_time.date():
                raise ValidationError('Date mismatch')

    @api.model
    def create(self, vals_list):
        vals_list['max_available_slots'] = vals_list['current_available_slots']

        return super(ShootBooking, self).create(vals_list)

    def name_get(self):
        result = []
        for rec in self:
            result.append((rec.id, rec.event_date_time))

        return result
