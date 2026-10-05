from odoo import models,fields

class Tags(models.Model):
    _name = 'tags'
    active = fields.Boolean(default=True)
    name=fields.Char()
    property_ids = fields.Many2many('property')


