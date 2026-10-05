from odoo import models, fields


class SaleOrder(models.Model):
    _inherit = 'sale.order'
    td_id = fields.Many2one('todo',string="ToDo_ID")


