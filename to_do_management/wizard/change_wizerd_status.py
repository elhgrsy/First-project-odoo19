from odoo import fields, models
from odoo.exceptions import ValidationError


class ChangeStatus(models.TransientModel):
    _name = 'change.status'
    _description = 'Change Status'
    status = fields.Selection([
        ('new', 'New')
        , ('in progress', 'In Progress')
        , ('completed', 'Completed')
    ], default='new')
    reason = fields.Char('Reason')
    todo_id = fields.Many2one('todo')

    def change_status(self):
        if self.todo_id.status == 'closed':
            self.todo_id.status = self.status
            self.todo_id.create_todo_history_record('closed' , self.status , self.reason)
        else:
             raise ValidationError('is not closed')

