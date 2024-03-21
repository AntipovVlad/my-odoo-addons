import logging

from odoo import http
from odoo.exceptions import ValidationError
from odoo.http import request

import json


_logger = logging.getLogger(__name__)


class InventoryBookingPage(http.Controller):
    @http.route('/inventory-booking/get-inventory/', auth="user", type="json", methods=['POST'])
    def inventory_booking_user(self, **kwargs):
        if kwargs['booking_type'] == 'single':
            inventory = request.env['product.product'].sudo().search([
                ('borrow_limit', '=', True)
            ])
            data = json.dumps({i: {'id': str(rec.id), 'name': str(rec.name)} for i, rec in enumerate(inventory)})

            return json.loads(data)

        if kwargs['booking_type'] == 'set':
            inventory = []
            for set_name_rec in request.env['product.product.set.names'].search([]):
                query = f"""
                    SELECT set.set_id, set.item_id, set.quantity, product.id, product.current_borrowed, stock.quantity, stock.product_id 
                    FROM product_product_set as set 
                    LEFT JOIN product_product as product ON set.item_id = product.id 
                    LEFT JOIN stock_quant as stock ON product.id = stock.product_id 
                    WHERE (set.quantity + product.current_borrowed <= stock.quantity) AND (set.set_id = {set_name_rec.id});
                """

                try:
                    request.cr.execute(query)
                except Exception as e:
                    _logger.error(f"====Transaction error====\n{e}")
                else:
                    available_set_items = len(request.env.cr.fetchall())
                    all_set_items = len(
                        request.env['product.product.set'].search([('set_id.id', '=', set_name_rec.id)]))

                    if all_set_items == available_set_items:
                        inventory.append((set_name_rec.id, set_name_rec.name))

            data = json.dumps({i: {'id': rec[0], 'name': rec[1]} for i, rec in enumerate(inventory)})

            return json.loads(data)

        raise ValidationError('Wrong parameters.')
