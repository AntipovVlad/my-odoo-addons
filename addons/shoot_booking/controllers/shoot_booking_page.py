from odoo import http
from odoo.http import request

from datetime import datetime

import json


class ShootBookingPage(http.Controller):
    @http.route('/shoot-booking/get-slots/', auth="public", type="json", methods=['POST'])
    def shoot_booking_public(self, **kwargs):
        free_slots = request.env['calendar.shoot_booking'].sudo().search([
            '&', ('current_available_slots', '!=', 0),
            ('event_date_time', '>', datetime.now()),
            ('crm_pipeline_id.id', '=', kwargs['team']),
            ('is_inside_slot', '=', kwargs['is_logged'])
        ])

        data = json.dumps({i: {'id': str(rec.id), 'dtime': str(rec.event_date_time)} for i, rec in enumerate(free_slots)})

        return json.loads(data)
