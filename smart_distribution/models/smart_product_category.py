from odoo import fields, models
class SmartProductCategory(models.Model):
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _name = 'smart.product.category'
    _description = 'Smart Product Category'
    name = fields.Char()
    description = fields.Char()
    active = fields.Boolean(default=True)
    product_ids = fields.One2many('smart.product','category_id',string='Products')

