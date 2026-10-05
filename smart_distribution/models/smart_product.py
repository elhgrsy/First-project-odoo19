from odoo import fields, models, api
from odoo.exceptions import ValidationError


class SmartProduct(models.Model):
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _name = 'smart.product'
    _description = 'Smart Product'
    _name_unique = models.Constraint('UNIQUE(name)', 'the name is unique')
    name = fields.Char(tracking=True, required=True)
    code = fields.Char(readonly=True, tracking=True, default='00000')
    description = fields.Text()
    price = fields.Float()
    cost = fields.Float()
    quantity = fields.Integer()
    active = fields.Boolean(default=True)
    category_id = fields.Many2one('smart.product.category')
    image = fields.Image()
    profit = fields.Float(compute='_computed_profit', tracking=True , store=True)
    profit_margin = fields.Float(compute='_computed_profit_margin', tracking=True , store=True)

    @api.constrains('code')
    def _check_code(self):
        for rec in self:
            if self.search([('code', '=', rec.code), ('id', '!=', rec.id)], limit=1):
                raise ValidationError('Code must be unique')

    @api.constrains('price', 'cost')
    def _check_price_cost(self):
        for rec in self:
            if rec.price < rec.cost:
                raise ValidationError('Must Be Price >= Cost')

    @api.depends('price', 'cost')
    def _computed_profit(self):
        for rec in self:
            rec.profit = rec.price - rec.cost
    @api.depends('price','profit')
    def _computed_profit_margin(self):
        for rec in self:
            if rec.price > 0 :
                 rec.profit_margin = (rec.profit/rec.price)
            else:
                rec.profit_margin = 0.0

    @api.model
    def create(self, vals):
        rec = super(SmartProduct, self).create(vals)
        if rec.code == '00000':
            rec.code = self.env['ir.sequence'].next_by_code('sequences_code')
        return rec
