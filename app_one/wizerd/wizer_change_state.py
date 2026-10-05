from odoo import models, fields
from odoo.exceptions import ValidationError


class ChangeState(models.TransientModel):
    _name = 'change.state'
    _description = 'Change State'
    property_id = fields.Many2one('property')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('pending', 'Pending'),
    ], default='draft')
    reason = fields.Char(string='Reason')

    def action_replace(self):
        if self.property_id.state == 'closed':
            self.property_id.state = self.state
            self.property_id.create_history_record('closed', self.state, self.reason)
        else:
            raise ValidationError("Is Not Closed")

