from datetime import timedelta

from odoo import models, fields, api
from odoo.exceptions import ValidationError



class Property(models.Model):
    _name = 'property'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Property'
    _rec_name = 'name'
    _name_unique = models.Constraint('UNIQUE(name)', 'replace name')
    # في الاصدراتن القديمه :(_sql_constraints = [])
    # اما في الاصدرات الحديثه (الاسم=models.constrains('UNIQUE(اسم الفلد)','الرساله'))
    owner_id = fields.Many2one('owner')
    ref=fields.Char(default='Naw' , readonly=1)
    active = fields.Boolean(default=True)
    tags_ids = fields.Many2many('tags')
    name = fields.Char(required="1" , tracking=True)
    # لو عايز اعدل البيانات في form view وعايزها تظهر فيchatter استخدم tracking=True
    description = fields.Text()
    postcode = fields.Char(required="1")
    phone = fields.Char(readonly="state == 'closed'") #تنفع في ملف البايثون و ملف xml (readonly="state == 'closed'")
    selling_price = fields.Float()
    bedrooms = fields.Integer()
    bathrooms = fields.Integer()
    btw_room = fields.Integer(
        compute='_compute_btw_room')  # (لتخزين البيانات نستخدم ,  store=True )( علي شان تخلي المستخدم يقدر يعدل في الاند يوزر,readonly = False)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection([('north', 'North'),
                                           ('south', 'South'),
                                           ('east', 'East'),
                                           ('west', 'West')
                                           ])
    state = fields.Selection([('draft', 'Draft'),
                              ('confirmed', 'Confirmed'),
                              ('pending', 'Pending'),
                              ('sold', 'Sold'),
                              ('closed', 'Closed'), ], default='draft')
    line_ids =fields.One2many('property.line', 'property_id', )
    pro_date=fields.Date()
    create_time=fields.Datetime(default=fields.Datetime.now())
    new_time=fields.Datetime(compute='_compute_new_time')
    is_lose=fields.Boolean()
    property_history_ids = fields.One2many('property.history', 'property_id',)
    # button

    def action_draft(self):
        for rec in self:
            rec.create_history_record(rec.state , 'draft' , "")
            rec.state = 'draft'  # او استخدام rec.write(['state':'draft])

    def action_pending(self):
        for rec in self:
            rec.create_history_record(rec.state , 'pending' , "")
            rec.write({'state': 'pending'})

    def action_confirmed(self):
        for rec in self:
            rec.create_history_record(rec.state , 'confirmed' , "")
            rec.write({'state': 'confirmed'})

    def action_sold(self):
        for rec in self:
            rec.create_history_record(rec.state , 'sold' , "")
            rec.state = 'sold'
    def action_closed(self):
        for rec in self:
            rec.create_history_record(rec.state , 'closed', "")
            rec.write({'state': 'closed'})
    @api.model
    def create_history_record(self , old_state , new_state , reason):
        for rec in self:
            rec.env['property.history'].create({
                'user_id': rec.env.uid,
                'property_id': rec.id,
                'old_state': old_state,
                'new_state': new_state,
                'reason': reason or "",
                'line_ids': [(0,0,{'description':line.description , 'area':line.area}) for line in rec.line_ids],
            })
    # -------------------------------------------------------------------------
    @api.model
    def action_open_change_state_wizerd(self):
        action = self.env['ir.actions.actions']._for_xml_id('app_one.record_wizerd_change_state_action')
        action['context'] = {'default_property_id':self.id}
        return action
    def owner_action(self):
        action = self.env['ir.actions.actions']._for_xml_id('app_one.owner_action_estate')
        view_id = self.env.ref('app_one.owner_action_form').id
        action['res_id']=self.owner_id.id
        action['views']=[[view_id , 'form']]
        return action
    # constrains ==> required = 1
    @api.constrains('garden_area')
    def _check_garden_area(self):
        for rec in self:
            if rec.garden_area == 0:
                raise ValidationError('enter garden_area')

    # -------------------------------------------------------------------------
    @api.depends('bedrooms', 'bathrooms' , 'create_time')
    def _compute_btw_room(self):
        for rec in self:
            rec.btw_room = rec.bedrooms + rec.bathrooms
    def _compute_new_time(self):
        for rec in self:
            if rec.create_time:
                rec.new_time = rec.create_time + timedelta(hours=6)


    @api.onchange('btw_room')
    def _compute_btw_rom(self):
       for rec in self:
           if rec.btw_room > 0:
               print("compute btw_room is true")
           else:
               print("compute btw_room is false")

    # -------------------------------------------------------------------------
    # @api.model_create_multi
    # def create(self, vals):
    #     rec = super(Property, self).create(vals)
    #     print("create is true")
    #     return rec

    @api.model
    # def _search(self, domain, offset=0, limit=None, order=None, access_right_uid=None, **kwargs):
    #     rec = super(Property, self)._search(domain, offset=0, limit=None, order=None, **kwargs)
    #     print("search is true")
    #     return rec

    def write(self, vals):
        rec = super(Property, self).write(vals)
        print("write is true")
        return rec

    def unlink(self):
        rec = super(Property, self).unlink()
        print("unlink is true")
        return rec
    @api.model
    def check_pro_date(self):
        pro_id=self.search([])
        for rec in pro_id:
            if rec.pro_date and rec.pro_date <= fields.Date.today():
                rec.is_lose=True
            else:
                rec.is_lose=False
            if rec.pro_date and rec.is_lose == True:
                rec.state = 'closed'
    def create(self,vals):
        rec = super(Property, self).create(vals)
        if rec.ref == 'Naw':
            rec.ref = self.env['ir.sequence'].next_by_code('property_seq')
        return rec
    # ------------------------------------------------------------------------------------------
class PropertyLine(models.Model):
    _name = 'property.line'
    _description = 'Property Line'
    property_id = fields.Many2one('property')
    area=fields.Float()
    description = fields.Text()
