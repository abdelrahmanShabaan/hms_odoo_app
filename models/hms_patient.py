from odoo import models, fields, api


class HmsPatient(models.Model):
    _name = 'hms.patient'
    _description = 'HMS Patient'
    _rec_name = 'first_name'

    first_name = fields.Char()
    last_name = fields.Char()
    birth_date = fields.Date()
    history = fields.Html()
    CR_ratio = fields.Float()
    blood_type = fields.Selection([('a', 'A'), ('b', 'B'), ('o', 'O')])
    PCR = fields.Boolean()
    image = fields.Image()
    address = fields.Text()
    age = fields.Integer()
    department_id = fields.Many2one('hms.department')
    capacity = fields.Integer(related='department_id.capacity')