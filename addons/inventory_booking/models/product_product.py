from odoo import models, fields, api


class InventorySetName(models.Model):
    _name = 'product.product.set.names'
    _description = 'Inventory set\'s names'

    name = fields.Char(string='Name of set', required=True)


class InventorySet(models.Model):
    _name = 'product.product.set'
    _description = 'Sets of inventory items'

    set_id = fields.Many2one(comodel_name='product.product.set.names', string='Set', index=True, required=True)
    item_id = fields.Many2one(comodel_name='product.product', string='Item', index=True, required=True)
    quantity = fields.Integer(string='Number of items', required=True)

    @api.model
    def create(self, vals_list):
        new_rec = super(InventorySet, self).create(vals_list)
        self.env['product.product'].search([('id', '=', vals_list['item_id'])])[0].write({'sets': [(4, new_rec.id)]})

        return new_rec

    def name_get(self):
        result = []
        for rec in self:
            result.append((rec.id, rec.set_id.name))

        return result


class ProductProductSetExtension(models.Model):
    _inherit = 'product.product'

    sets = fields.Many2many(comodel_name='product.product.set', ondelete='cascade')
    current_borrowed = fields.Float(string='Current number of items', default=0.0)
    borrow_limit = fields.Boolean(string='Borrow limit', compute='_check_if_can_be_borrowed', store=True)

    @api.depends('current_borrowed')
    def _check_if_can_be_borrowed(self):
        for rec in self:
            rec.borrow_limit = rec.current_borrowed < rec.qty_available

