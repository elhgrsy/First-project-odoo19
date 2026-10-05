from odoo import models,fields

class Owner(models.Model):
    _name = 'owner'
    active = fields.Boolean(default=True)
    property_ids = fields.One2many('property', 'owner_id')
    name=fields.Char()
    address=fields.Char()
    phone_number=fields.Char()
    email_owner=fields.Char()

