from docutils.nodes import address

from odoo import models, fields, api


class ToDo(models.Model):
    _name = 'todo'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'ToDoManagement'
    active = fields.Boolean(default=True)  # بيخف او بيظهر الداتا مجده في خانه الاعددات الي فياها الحذف و الحفظ
    name = fields.Char(required=True)
    selling_date = fields.Date()
    is_late = fields.Boolean()
    description = fields.Char()
    assign_to = fields.Many2one('res.users', required=True)
    due_date = fields.Date()
    status = fields.Selection([('new', 'New')
                                  , ('in progress', 'In Progress')
                                  , ('completed', 'Completed')
                                  , ('closed', 'Closed')])
    line_ids = fields.One2many('todo.line', 'todo_id')
    ref = fields.Char(default='New', readonly=True)

    def action_new(self):
        for rec in self:
            rec.create_todo_history_record(rec.status , 'new',"")
            rec.status = 'new'

    def action_in_progress(self):
        for rec in self:
            rec.create_todo_history_record(rec.status , 'in progress',"")
            rec.status = 'in progress'

    def action_complete(self):
        for rec in self:
            rec.create_todo_history_record(rec.status , 'completed',"")
            rec.status = 'completed'

    def action_closed(self):
        for rec in self:
            rec.create_todo_history_record(rec.status , 'closed',"")
            rec.status = 'closed'

    @api.model
    def create_todo_history_record(self , old_status , new_status , reason):
        for rec in self:
            rec.env['todo.history'].create({
                'user_id' : rec.env.uid,
                'todo_id' : rec.id,
                'old_status' : old_status,
                'new_status' : new_status,
                'reason' : reason or "",
                'line_ids' : [(0,0,{'phone': line.phone , 'address': line.address}) for line in rec.line_ids],
            })
    @api.model
    def action_wizard_open_change_status_window(self):
        action = self.env['ir.actions.actions']._for_xml_id('to_do_management.change_status_action')
        action['context'] = {'default_todo_id': self.id}
        return action


    def check_selling_date(self):
        todo_ids = self.search([])
        for rec in todo_ids:
            if rec.selling_date and rec.selling_date < fields.Date.today():
                rec.is_late = True
            else:
                rec.is_late = False
            if rec.selling_date and rec.is_late == True:
                rec.status = 'closed'

    def create(self, vals):
        rec = super(ToDo, self).create(vals)
        if rec.ref == 'New':
            rec.ref = self.env['ir.sequence'].next_by_code('pro_sequences')
        return rec
class ToDoLine(models.Model):
    _name = 'todo.line'
    _description = 'ToDoLine'
    todo_id = fields.Many2one('todo')
    phone = fields.Char()
    address = fields.Char()
