from odoo import models, fields


class ToDoHistory(models.Model):
    _name = 'todo.history'
    _description = 'ToDoManagement'
    user_id = fields.Many2one('res.users')
    todo_id = fields.Many2one('todo')
    old_status = fields.Char()
    new_status = fields.Char()
    reason = fields.Char()

    line_ids = fields.One2many('history.line', 'history_id')



class ToDoHistoryLine(models.Model):
    _name = 'history.line'

    history_id = fields.Many2one('todo.history')
    phone = fields.Char()
    address = fields.Char()



