import logging
from datetime import date, datetime

from odoo import models, fields, api
from odoo.exceptions import ValidationError


_logger = logging.getLogger(__name__)


class StockRent(models.Model):
    _name = 'stock.rent'
    _description = 'Model for items rent'

    product_type = fields.Selection(selection=[('single', 'Предмет'),
                                               ('set', 'Комплект')],
                                    string='Inventory type',
                                    default='single')
    item_id = fields.Many2one(comodel_name='product.product', string='Inventory item', default=False)
    set_id = fields.Many2one(comodel_name='product.product.set.names', string='Inventory set', default=False)
    inventory = fields.Reference(selection=[('product.product', 'Предмет'),
                                            ('product.product.set.names', 'Комплект')],
                                 string='Inventory', compute='_create_inventory')

    person_name = fields.Char(string='Person', required=True)
    quantity = fields.Float(string='Quantity on hand', default=0.0)
    return_date = fields.Date(string='Deadline', required=True)
    is_returned = fields.Boolean(string='Is item returned', default=False)

    def _create_inventory(self):
        for rec in self:
            if rec.product_type == 'single':
                rec['inventory'] = f"product.product,{rec.item_id.id}"
            elif rec.product_type == 'set':
                rec['inventory'] = f"product.product.set.names,{rec.set_id.id}"

    @api.model
    def create(self, vals_list: dict):
        try:
            new_rec = super(StockRent, self).create(vals_list)
        except Exception as e:
            _logger.error(f"====Transaction error====\n{e}")
            raise ValidationError('Incorrect data in fields.')
        else:
            wrong_params_combo = (vals_list.get('item_id') and vals_list.get('set_id')) or \
                    (vals_list.get('item_id') is None and vals_list.get('set_id') is None)
            if wrong_params_combo:
                raise ValidationError('Incorrect data in fields.')

            if vals_list.get('item_id') and vals_list.get('item_id') > 0:
                product_rec = self.env['product.product'].search([('id', '=', vals_list.get('item_id'))])[0]
                if (new_sum := vals_list.get('quantity') + product_rec.current_borrowed) <= product_rec.qty_available:
                    product_rec.write({'current_borrowed': new_sum})
                else:
                    raise ValidationError('Item quantity error.')

            if vals_list.get('set_id') and vals_list.get('set_id') > 0:
                set_quantity = 0
                for rec in self.env['product.product.set'].search([('set_id', '=', vals_list.get('set_id'))]):
                    product_rec = self.env['product.product'].search([('id', '=', rec.item_id.id)])[0]
                    set_quantity += rec.quantity
                    if (new_sum := rec.quantity + product_rec.current_borrowed) <= product_rec.qty_available:
                        product_rec.write({'current_borrowed': new_sum})
                    else:
                        raise ValidationError('Set quantity error.')

                new_rec.write({'quantity': set_quantity})

            if not (vals_list.get('return_date') and
                    datetime.strptime(vals_list.get('return_date'), '%Y-%m-%d').date() > date.today()):
                raise ValidationError('Incorrect date.')

            return new_rec

    def __product_return(self):
        if self.product_type == 'single':
            product = self.env['product.product'].search([('id', '=', self.item_id.id)])[0]
            product.write({'current_borrowed': product.current_borrowed - self.quantity})
        elif self.product_type == 'set':
            for rec in self.env['product.product.set'].search([('set_id.id', '=', self.set_id.id)]):
                product_rec = self.env['product.product'].search([('id', '=', rec.item_id.id)])[0]
                product_rec.write({'current_borrowed': product_rec.current_borrowed - rec.quantity})

    def unlink(self):
        for rec in self:
            if not rec.is_returned:
                rec.__product_return()
        return super(StockRent, self).unlink()

    def write(self, vals):
        if vals.get('is_returned'):
            self.__product_return()

        return super(StockRent, self).write(vals)

    def action_open_label_layout(self):
        return super(StockRent, self).action_open_label_layout()

    def action_update_quantity_on_hand(self):
        return super(StockRent, self).action_update_quantity_on_hand()
